from __future__ import annotations

import discord


def get_nickname(user: discord.User | discord.Member) -> str:
    """
    Returns a nickname for a given Discord user

    Prioritizes in order: server nickname, global display name, username
    """
    if isinstance(user, discord.Member) and user.nick is not None:
        return user.nick

    if user.global_name is not None:
        return user.global_name

    return user.name


def get_emoji_url(emoji_id: int) -> str:
    """Return emoji URL for a given ID"""
    return f'https://cdn.discordapp.com/emojis/{emoji_id}.png'
