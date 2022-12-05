from abc import ABC, abstractmethod

import discord

from walnut.irc.message import Message as IRCMessage


class BaseHook(ABC):
    """ABC for a Walnut IRC/Discord dual hook"""

    @abstractmethod
    async def handle_irc_message(self, message: IRCMessage) -> None:
        ...

    @abstractmethod
    async def handle_discord_message(self, message: discord.Message) -> None:
        ...
