# Source: https://github.com/sopel-irc/sopel/blob/fdc1d165/sopel/formatting.py
#
# Copyright 2014, Elsie Powell, embolalia.com
# Copyright 2019, dgw, technobabbl.es
# Copyright 2022, Velocidensity (adapted from sopel for Walnut, see NOTICE.md for the license text)
# Licensed under the Eiffel Forum License 2.
from __future__ import annotations

import re
from enum import Enum

__all__ = [
    # control chars
    'CONTROL_NORMAL',
    'CONTROL_COLOR',
    'CONTROL_HEX_COLOR',
    'CONTROL_BOLD',
    'CONTROL_ITALIC',
    'CONTROL_UNDERLINE',
    'CONTROL_STRIKETHROUGH',
    'CONTROL_MONOSPACE',
    'CONTROL_REVERSE',
    # utility functions
    'color',
    'bold',
    'italic',
    'underline',
    'strikethrough',
    'plain',
    # utility enum
    'Colors',
]

# Color names are as specified at http://www.mirc.com/colors.html

CONTROL_NORMAL = '\x0f'
"""The control code to reset formatting."""
CONTROL_COLOR = '\x03'
"""The control code to start or end color formatting."""
CONTROL_HEX_COLOR = '\x04'
"""The control code to start or end hexadecimal color formatting."""
CONTROL_BOLD = '\x02'
"""The control code to start or end bold formatting."""
CONTROL_ITALIC = '\x1d'
"""The control code to start or end italic formatting."""
CONTROL_UNDERLINE = '\x1f'
"""The control code to start or end underlining."""
CONTROL_STRIKETHROUGH = '\x1e'
"""The control code to start or end strikethrough formatting."""
CONTROL_MONOSPACE = '\x11'
"""The control code to start or end monospace formatting."""
CONTROL_REVERSE = '\x16'
"""The control code to start or end reverse-color formatting."""

CONTROL_FORMATTING = [
    CONTROL_NORMAL,
    CONTROL_COLOR,
    CONTROL_HEX_COLOR,
    CONTROL_BOLD,
    CONTROL_ITALIC,
    CONTROL_UNDERLINE,
    CONTROL_STRIKETHROUGH,
    CONTROL_MONOSPACE,
    CONTROL_REVERSE,
]
"""A list of all control characters expected to appear as formatting."""

CONTROL_NON_PRINTING = [
    '\x00',
    '\x01',
    '\x02',  # CONTROL_BOLD
    '\x03',  # CONTROL_COLOR
    '\x04',  # CONTROL_HEX_COLOR
    '\x05',
    '\x06',
    '\x07',
    '\x08',
    '\x09',
    '\x0a',
    '\x0b',
    '\x0c',
    '\x0d',
    '\x0e',
    '\x0f',  # CONTROL_NORMAL
    '\x10',
    '\x11',  # CONTROL_MONOSPACE
    '\x12',
    '\x13',
    '\x14',
    '\x15',
    '\x16',  # CONTROL_REVERSE
    '\x17',
    '\x18',
    '\x19',
    '\x1a',
    '\x1b',
    '\x1c',
    '\x1d',  # CONTROL_ITALIC
    '\x1e',  # CONTROL_STRIKETHROUGH
    '\x1f',  # CONTROL_UNDERLINE
    '\x7f',
]

# Regex to detect Control Pattern
COLOR_PATTERN = re.escape(CONTROL_COLOR) + r'((\d{1,2},\d{2})|\d{2})?'
HEX_COLOR_PATTERN = '%s(%s)?' % (
    re.escape(CONTROL_HEX_COLOR),
    '|'.join([
        '(' + ','.join([r'[a-fA-F0-9]{6}', r'[a-fA-F0-9]{6}']) + ')',
        r'[a-fA-F0-9]{6}'
    ])
)

PLAIN_PATTERN = '|'.join([
    '(' + COLOR_PATTERN + ')',
    '(' + HEX_COLOR_PATTERN + ')',
])
PLAIN_REGEX = re.compile(PLAIN_PATTERN)


class Colors(str, Enum):
    """Mapping of color names to mIRC code values."""
    # Mostly aligned with https://modern.ircdocs.horse/formatting.html#colors
    # which are likely based on mIRC's color names (https://www.mirc.com/colors.html)
    WHITE = '00'
    BLACK = '01'
    BLUE = '02'
    GREEN = '03'
    LIGHT_RED = '04'
    BROWN = '05'
    PURPLE = '06'
    ORANGE = '07'
    YELLOW = '08'
    LIGHT_GREEN = '09'
    CYAN = '10'
    LIGHT_CYAN = '11'
    LIGHT_BLUE = '12'
    PINK = '13'
    GREY = '14'
    LIGHT_GREY = '15'


def _get_color(color: str | int | None) -> str | None:
    """Return the text, with the given colors applied in IRC formatting.

    :param str color: color name or number
    :raises ValueError: if ``color`` is an unrecognized color value

    The color can be a string of the color name, or an integer in the range
    0-99. The known color names can be found in the :class:`colors` class of
    this module.
    """
    if color is None:
        return None

    # You can pass an int or string of the code
    try:
        color = int(color)
    except ValueError:
        pass
    if isinstance(color, int):
        if color > 99:
            raise ValueError('Can not specify a color above 99.')
        return str(color).rjust(2, '0')

    # You can also pass the name of the color
    color_name = color.upper()
    color_dict = Colors.__dict__
    try:
        return color_dict[color_name]
    except KeyError:
        raise ValueError('Unknown color name {}'.format(color))


def color(text: str, fg: str | int | None = None, bg: str | int | None = None) -> str:
    """Return the text, with the given colors applied in IRC formatting.

    :param str text: the text to format
    :param mixed fg: the foreground color
    :param mixed bg: the background color
    :raises TypeError: if ``text`` is not a string
    :raises ValueError: if ``color`` is an unrecognized color value

    The color can be a string of the color name, or an integer in the range
    0-99. The known color names can be found in the :class:`colors` class of
    this module.
    """
    if color is None:
        return text

    fg = _get_color(fg) or ''
    bg = _get_color(bg) or ''

    if bg:
        return ''.join([CONTROL_COLOR, fg or '', ',', bg, text, CONTROL_COLOR])
    return ''.join([CONTROL_COLOR, fg or '', text, CONTROL_COLOR])


def bold(text: str) -> str:
    """Return the text, with bold IRC formatting.

    :param str text: the text to format
    :raises TypeError: if ``text`` is not a string
    """
    return ''.join([CONTROL_BOLD, text, CONTROL_BOLD])


def italic(text: str) -> str:
    """Return the text, with italic IRC formatting.

    :param str text: the text to format
    :raises TypeError: if ``text`` is not a string
    """
    return ''.join([CONTROL_ITALIC, text, CONTROL_ITALIC])


def underline(text: str) -> str:
    """Return the text, with underline IRC formatting.

    :param str text: the text to format
    :raises TypeError: if ``text`` is not a string
    """
    return ''.join([CONTROL_UNDERLINE, text, CONTROL_UNDERLINE])


def strikethrough(text: str) -> str:
    """Return the text, with strikethrough IRC formatting.

    :param str text: the text to format
    :raises TypeError: if ``text`` is not a string
    """
    return ''.join([CONTROL_STRIKETHROUGH, text, CONTROL_STRIKETHROUGH])


def plain(text: str) -> str:
    """Return the text without any IRC formatting.

    :param str text: text with potential IRC formatting control code(s)
    :raises TypeError: if ``text`` is not a string
    """
    if '\x03' in text or '\x04' in text:
        text = PLAIN_REGEX.sub('', text)
    return ''.join(c for c in text if ord(c) >= 0x20 and c != '\x7F')
