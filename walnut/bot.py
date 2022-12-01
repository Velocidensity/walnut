import asyncio
from collections.abc import Callable

import discord
from pyrcb2 import Event, IRCBot, IStr, Sender

from walnut.config import CONFIG
from walnut.irc.message import Message as IRCMessage


class WalnutBot:
    """Main class handling the bot"""

    def __init__(self):
        """Initializes Discord and IRC clients"""
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.discord = discord.Client(intents=intents)
        # since we can't call self.discord.Event as a decorator, we do it manually
        self.discord.on_message = self._on_discord_message
        self.tree = discord.app_commands.CommandTree(self.discord)

        self.irc = IRCBot(log_communication=True)
        self.irc.load_events(self)

        self.irc_hooks: list[Callable] = []
        self.discord_hooks: list[Callable] = []

    def run(self):
        """Starts the bot and connects to Discord and IRC"""
        loop = asyncio.new_event_loop()
        loop.create_task(self.discord.start(CONFIG['discord']['token']))
        loop.create_task(self.irc.run(self._on_irc_connect()))
        loop.run_forever()

    def add_discord_command(
        self,
        command: discord.app_commands.Command | discord.app_commands.ContextMenu | discord.app_commands.Group
    ):
        """Adds a Discord command to the CommandTree"""
        return self.tree.add_command(command)

    async def _on_irc_connect(self):
        await self.irc.connect("irc.rizon.net", 6697, ssl=True)
        await self.irc.register("wnttest")
        for relay in CONFIG['relays']:
            await self.irc.join(relay['irc_channel'])

    @Event.privmsg
    async def _on_irc_message(self, sender: Sender, channel: IStr, message: str):
        obj = IRCMessage(self.irc, sender, channel, message)
        for hook in self.irc_hooks:
            await hook(obj)

    async def _on_discord_message(self, message: discord.Message):
        for hook in self.discord_hooks:
            await hook(message)
