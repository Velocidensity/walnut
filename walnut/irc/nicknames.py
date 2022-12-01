from __future__ import annotations

import discord

from walnut.irc.formatting import color

NICK_COLORS = ['LIGHT_BLUE', 'BLUE', 'LIGHT_RED', 'RED', 'LIGHT_GREEN',
               'GREEN', 'PURPLE', 'PINK', 'ORANGE', 'YELLOW', 'CYAN', 'LIGHT_CYAN']
NON_BREAKING_SPACE = '\u200b'


def sanitize_nickname(nickname: str) -> str:
    """Adds a non-breaking space to a nickname prevent pinging"""
    return nickname[0] + NON_BREAKING_SPACE + nickname[1:]


def select_color(nickname: str) -> str:
    """Selects a color tag for a given nickname"""
    color_id = int((ord(nickname[0]) + len(nickname)) / len(NICK_COLORS))
    selected_color = NICK_COLORS[color_id]
    return selected_color


def format_discord_user(
    user: discord.User | discord.Member,
    colorize: bool = True,
    use_nickname: bool = True,
    use_username: bool = False,
    prevent_pinging: bool = True
) -> str:
    """
    Returns an IRC-formatted string representation of a Discord user/member

    :param user: an object representing a Discord user/member
    :param colorize: toggles nickname colorization (based on global username for consistency)
    :param use_nickname: toggles displaying server nickname instead of global usernames
    :param use_username: toggles displaying global usernames next to nicknames
    :param prevent_pinging: prevents pinging the message author
    :param sanitized_names: optional list of nicknames to sanitize
    """
    def _sanitize(nickname: str) -> str:
        if prevent_pinging:
            return sanitize_nickname(nickname)
        return nickname

    if isinstance(user, discord.Member):
        name = _sanitize(user.nick or user.name if use_nickname else user.name)
        if use_username and user.nick:
            name += f' ({_sanitize(user.name)})'
    else:
        name = _sanitize(user.name)

    if colorize:
        selected_color = select_color(user.name)
        return color(name, selected_color)

    return name
