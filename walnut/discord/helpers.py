from __future__ import annotations

import discord


def get_nicknames(user: discord.User | discord.Member) -> list[str]:
    """Returns a list of all names for a given Discord user"""
    if isinstance(user, discord.Member) \
            and user.nick is not None and user.nick != user.name:
        return [user.nick, user.name]

    return [user.name]
