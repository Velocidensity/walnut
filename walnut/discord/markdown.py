from __future__ import annotations

import re

import mistune
from mistune.plugins.formatting import PREVENT_BACKSLASH, _parse_to_end

__all__ = ['EMOJI_REGEX', 'discord_spoiler', 'discord_emoji']

EMOJI_REGEX = re.compile(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>')
_SPOILER_END = re.compile(r'(?:' + PREVENT_BACKSLASH + r'\\~|[^\s~])\|\|(?!~)')


def _parse_discord_spoiler(
    inline: mistune.InlineParser,
    match: re.Match,
    state: mistune.BlockState | mistune.InlineState
):
    return _parse_to_end(inline, match, state, 'discord_spoiler', _SPOILER_END)


def discord_spoiler(md: mistune.Markdown):
    """Mistune plugin adding support for Discord spoiler tags"""
    md.inline.register(
        'discord_spoiler',
        r'\|\|(?=[^\s~])',
        _parse_discord_spoiler
    )


def _parse_discord_emoji(_, m: re.Match, state: mistune.BlockState | mistune.InlineState):
    state.append_token({
        'type': 'discord_emoji',
        'text': m.group('name'),
        'attrs': {
            'emoji_id': int(m.group('id')),
            'animated': bool(m.group('animated'))
        }
    })
    return m.end() + 1


def discord_emoji(md: mistune.Markdown):
    """Mistune plugin adding support for Discord emoji representation"""
    md.inline.register(
        'discord_emoji',
        EMOJI_REGEX.pattern,
        _parse_discord_emoji
    )
