from abc import ABC, abstractmethod

import discord

from walnut.bot import WalnutBot
from walnut.irc.message import Message as IRCMessage


class BaseHook(ABC):
    """Abstract base class for a Walnut IRC/Discord dual hook"""

    @abstractmethod
    async def handle_irc_message(self, message: IRCMessage) -> None:
        """Processes an incoming IRC message"""
        ...

    @abstractmethod
    async def handle_discord_message(self, message: discord.Message) -> None:
        """Processes an incoming Discord message"""
        ...

    @abstractmethod
    def load(self, bot: WalnutBot) -> None:
        """Loads the relay into the bot"""
        ...
