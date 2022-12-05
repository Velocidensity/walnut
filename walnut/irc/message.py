from asyncio.futures import Future
from dataclasses import dataclass

from pyrcb2.itypes import IStr, Sender
from pyrcb2.pyrcb2 import IRCBot


@dataclass
class Message:
    """Representation of a IRC message, similar to discord.Message"""
    context: IRCBot
    sender: Sender
    channel: IStr
    content: str

    @property
    def author(self) -> Sender:
        return self.sender

    async def reply(self, content: str) -> Future:
        """Sends a reply to the source channel"""
        return self.context.privmsg(self.channel, content)
