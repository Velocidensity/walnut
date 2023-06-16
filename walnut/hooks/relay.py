from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, cast

import aiohttp
import discord
from discord.abc import Messageable
from mistune import InlineParser, Markdown
from mistune.plugins.formatting import strikethrough
from pyrcb2.itypes import IStr

from walnut.bot import WalnutBot
from walnut.config import RelayConfig
from walnut.discord.helpers import get_emoji_url
from walnut.discord.markdown import EMOJI_REGEX, discord_emoji, discord_spoiler
from walnut.hooks.base import BaseHook
from walnut.irc.markdown import IRCRenderer
from walnut.irc.message import Message as IRCMessage
from walnut.irc.nicknames import format_discord_user

if TYPE_CHECKING:
    from discord.abc import PrivateChannel
    from discord.guild import GuildChannel
    from discord.threads import Thread


parse_markdown = cast(Callable[[str], str], Markdown(
    renderer=IRCRenderer(),
    inline=InlineParser(hard_wrap=False),
    plugins=[strikethrough, discord_spoiler, discord_emoji]
))


class MessageRelay(BaseHook):
    """Discord/IRC message relay class"""
    colorize_irc_nicknames: bool = True
    use_discord_nicknames: bool = True
    use_discord_usernames_with_nicknames: bool = True
    prevent_self_pinging: bool = True
    expand_emotes: bool = True
    enable_stickers: bool = True

    def __init__(
        self,
        irc_channel: str,
        discord_channel_id: int,
        discord_webhook_url: str | None = None,
    ):
        self.bot: WalnutBot | None = None
        self.irc_channel = cast(IStr, irc_channel)
        self.discord_channel: GuildChannel | Thread | PrivateChannel | None = None
        self.discord_channel_id = discord_channel_id
        self.discord_webhook_url = discord_webhook_url

    @classmethod
    def from_config(cls, config: RelayConfig):
        """Initializes a MessageRelay from a RelayConfig"""
        relay = cls(
            irc_channel=config.irc_channel,
            discord_channel_id=config.discord_channel_id,
            discord_webhook_url=config.discord_webhook_url
        )
        for key, value in config.__dict__.items():
            setattr(relay, key, value)

        return relay

    def load(self, bot: WalnutBot) -> None:
        """Loads the relay into the bot"""
        self.bot = bot
        bot.irc_hooks.append(self.handle_irc_message)
        bot.discord_hooks.append(self.handle_discord_message)

    async def handle_irc_message(self, message: IRCMessage) -> None:
        """Handles and relays an IRC message"""
        if not self.bot:
            raise RuntimeError('Relay not loaded, Relay.load(bot) must be called first')

        if message.channel != self.irc_channel:
            return

        if not self.discord_channel:
            self.discord_channel = self.bot.discord.get_channel(self.discord_channel_id)

        if not isinstance(self.discord_channel, Messageable):
            raise ValueError('Given Discord channel ID is not a messageable channel')

        # Prefer sending message via a Discord webhook
        if self.discord_webhook_url:
            member = self.discord_channel.guild.get_member_named(message.author)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    url=self.discord_webhook_url,
                    session=session
                )

                if not hasattr(webhook, 'send'):
                    raise RuntimeError('Resolved Webhook has no send()')

                await webhook.send(  # type: ignore[attr-defined]
                    username=message.author,
                    avatar_url=member.avatar.url if member and member.avatar else None,
                    content=message.content
                )
            return

        await self.discord_channel.send(f'<{message.sender}> {message}')

    async def handle_discord_message(self, message: discord.Message) -> None:
        """Handles and relays a Discord message"""
        if not self.bot:
            raise RuntimeError('Relay not loaded, Relay.load(bot) must be called first')

        if message.author.bot or message.channel.id != self.discord_channel_id:
            return

        nickname = self.format_discord_user(message.author)

        reply = ''
        if message.reference and message.reference.cached_message:
            reference_author = self.format_discord_user(
                message.reference.cached_message.author,
                colorize=False
            )
            reply = f'[Replying to {reference_author}] '

        # Handle stickers first. API supports multiple, but clients do not
        for sticker in message.stickers:
            return await self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> Sticker: {sticker.name} ({sticker.url})'
            )

        # Treat emoji-only messages similar to stickers
        if m := re.match(EMOJI_REGEX, message.content):
            # discord.py's get_emoji relies on the emoji being from a shared server
            # and ID is sufficient to get the image URL
            emoji_url = get_emoji_url(int(m.group('id')))
            await self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> Emoji: {m.group("name")} {emoji_url}'
            )
        # Regular message, still want to strip out emoji IDs (<:emote:12345> -> :emote:)
        else:
            parsed = parse_markdown(cast(str, message.clean_content))
            if parsed.count('\n') > 3:  # preserve new lines without spam
                parsed = parsed.replace('\n', ' ')

            for part in parsed.splitlines():
                await self.bot.irc.privmsg(
                    self.irc_channel,
                    f'<{nickname}> {reply}' + part
                )

        # Send each attachment as a separate message with the URL
        for attachment in message.attachments:
            await self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> {attachment.url}'
            )

    def format_discord_user(self, user: discord.User | discord.Member, **kwargs) -> str:
        params = dict(
            colorize=self.colorize_irc_nicknames,
            use_nickname=self.use_discord_nicknames,
            use_username=self.use_discord_usernames_with_nicknames,
            prevent_pinging=self.prevent_self_pinging,
        )
        params.update(kwargs)
        return format_discord_user(user, **params)
