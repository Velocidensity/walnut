from __future__ import annotations

import re
from typing import Callable, cast

import aiohttp
import discord
from discord.abc import Messageable
from mistune import InlineParser, Markdown
from pyrcb2 import IStr

from walnut.bot import WalnutBot
from walnut.config import RelayConfig
from walnut.discord.markdown import EMOJI_REGEX, discord_emoji, discord_spoiler
from walnut.irc.markdown import IRCRenderer
from walnut.irc.message import Message as IRCMessage
from walnut.irc.nicknames import format_discord_user

parse_markdown = cast(Callable[[str], str], Markdown(
    renderer=IRCRenderer(),
    inline=InlineParser(hard_wrap=False),
    plugins=['strikethrough', discord_spoiler, discord_emoji]
))


class MessageRelay:
    """Message relay class"""
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
        self.bot = None
        self.irc_channel = IStr(irc_channel)
        self.discord_channel = None
        self.discord_channel_id = discord_channel_id
        self.discord_webhook_url = discord_webhook_url

    @classmethod
    def from_config(cls, config: RelayConfig):
        """Initializes a MessageRelay from a RelayConfig"""
        return cls(**config.__dict__)

    def load(self, bot: WalnutBot):
        """Loads the relay into the bot"""
        self.bot = bot
        bot.irc_hooks.append(self.handle_irc_message)
        bot.discord_hooks.append(self.handle_discord_message)

    async def handle_irc_message(self, message: IRCMessage):
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

                await webhook.send(
                    username=message.author,
                    avatar_url=member.avatar.url if member and member.avatar else None,
                    content=message.content
                )
            return

        await self.discord_channel.send(f'<{message.sender}> {message}')

    async def handle_discord_message(self, message: discord.Message):
        """Handles and relays a Discord message"""
        if not self.bot:
            raise RuntimeError('Relay not loaded, Relay.load(bot) must be called first')

        if message.author == self.bot.discord.user or message.author.bot:
            return

        if 'sync dupa' in message.content:
            await self.bot.tree.sync()
            await message.reply('synced dupa')
            return

        nickname = format_discord_user(
            user=message.author,
            colorize=self.colorize_irc_nicknames,
            use_nickname=self.use_discord_nicknames,
            use_username=self.use_discord_usernames_with_nicknames,
            prevent_pinging=self.prevent_self_pinging,
        )

        # Handle stickers first. API supports multiple, but clients do not
        for sticker in message.stickers:
            return await self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> Sticker: {sticker.name} ({sticker.url})'
            )

        # Treat emoji-only messages similar to stickers
        if m := re.match(EMOJI_REGEX, message.content):
            emoji = self.bot.discord.get_emoji(int(m.group('id')))
            self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> Emoji: {m.group("name")}' + (f' ({emoji.url})' if emoji else '')
            )
        # Regular message, still want to strip out emoji IDs (<:emote:12345> -> :emote:)
        else:
            parsed = parse_markdown(message.clean_content)
            if parsed.count('\n') > 3:  # preserve new lines without spam
                parsed = parsed.replace('\n', ' ')

            for part in parsed.splitlines():
                self.bot.irc.privmsg(
                    self.irc_channel,
                    f'<{nickname}> ' + part
                )

        # Send each attachment as a separate message with the URL
        for attachment in message.attachments:
            self.bot.irc.privmsg(
                self.irc_channel,
                f'<{nickname}> {attachment.url}'
            )
