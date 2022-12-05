import asyncio
from typing import Any, Callable, Coroutine

import discord
from pyrcb2.events import Event
from pyrcb2.itypes import IStr, Sender
from pyrcb2.pyrcb2 import IRCBot

from walnut.config import Config
from walnut.irc.message import Message as IRCMessage


class WalnutBot:
    """Main class handling the bot"""

    def __init__(self, config: Config):
        """Initializes Discord and IRC clients"""
        self.config = config

        intents = discord.Intents.default()
        intents.members = True  # type: ignore[assignment]
        intents.message_content = True  # type: ignore[assignment]

        self.discord = discord.Client(intents=intents)
        # since we can't call self.discord.Event as a decorator, we do it manually
        self.discord.on_message = self._on_discord_message  # type: ignore[attr-defined]
        self.tree = discord.app_commands.CommandTree(self.discord)

        self.irc = IRCBot(log_communication=True)
        self.irc.load_events(self)

        self.irc_hooks: list[Callable[[IRCMessage], Coroutine[Any, Any, None]]] = []
        self.discord_hooks: list[Callable[[discord.Message], Coroutine[Any, Any, None]]] = []

    def run(self) -> None:
        """Starts the bot and connects to Discord and IRC"""
        loop = asyncio.new_event_loop()
        loop.create_task(self.discord.start(self.config.discord_token))
        loop.create_task(self.irc.run(self._on_irc_connect()))
        loop.run_forever()

    def add_discord_command(
        self,
        command: discord.app_commands.Command | discord.app_commands.ContextMenu | discord.app_commands.Group
    ) -> None:
        """Adds a Discord command to the CommandTree"""
        return self.tree.add_command(command)

    async def _on_irc_connect(self) -> None:
        await self.irc.connect(
            hostname=self.config.irc_config.server,
            port=self.config.irc_config.port,
            ssl=self.config.irc_config.ssl
        )
        await self.irc.register(
            nickname=self.config.irc_config.nickname,
            username=self.config.irc_config.username,
            realname=self.config.irc_config.realname,
            password=self.config.irc_config.password
        )

        for relay in self.config.relays:
            await self.irc.join(relay.irc_channel)

    @Event.privmsg  # type: ignore[attr-defined]
    async def _on_irc_message(self, sender: Sender, channel: IStr, message: str) -> None:
        obj = IRCMessage(self.irc, sender, channel, message)
        for hook in self.irc_hooks:
            await hook(obj)

    async def _on_discord_message(self, message: discord.Message) -> None:
        for hook in self.discord_hooks:
            await hook(message)
