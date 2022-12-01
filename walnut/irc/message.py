from dataclasses import dataclass

from pyrcb2 import IRCBot, IStr, Sender


@dataclass
class Message:
    """Representation of a IRC message, similar to discord.Message"""
    context: IRCBot
    sender: Sender
    channel: IStr
    content: str

    @property
    def author(self):
        return self.sender

    async def reply(self, content: str):
        """Sends a reply to the source channel"""
        return self.context.privmsg(self.channel, content)
