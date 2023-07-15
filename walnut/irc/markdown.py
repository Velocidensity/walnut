from __future__ import annotations

import mistune

from walnut.irc.formatting import Colors, bold, color, italic, strikethrough


class IRCRenderer(mistune.BaseRenderer):
    """A renderer representing Markdown text as IRC formatting"""
    NAME = 'irc'

    def render_token(self, token: dict, state: mistune.BlockState | mistune.InlineState):
        func = self._get_method(token['type'])
        attrs = {}

        text = None
        if 'raw' in token:
            text = token['raw']
        elif 'children' in token:
            text = self.render_tokens(token['children'], state)
        elif 'text' in token:
            text = token['text']

        if text:
            attrs['text'] = text

        if 'attrs' in token:
            attrs.update(token['attrs'])

        return func(**attrs)

    def strong(self, text: str) -> str:
        return bold(text)

    def emphasis(self, text: str) -> str:
        return italic(text)

    def strikethrough(self, text: str) -> str:
        return strikethrough(text)

    def link(self, text: str, url: str, title: str | None = None) -> str:
        if text == url:
            output = text
        else:
            output = f'{url} ({text})'
        if title and title not in (text, url):
            output = f'{output} ({title})'

        return output

    def image(self, text: str, url: str, title: str | None = None) -> str:
        return self.link(text, url, title)

    def block_quote(self, text: str) -> str:
        return '\n'.join(f'> {part}' for part in text.splitlines())

    def codespan(self, text: str) -> str:
        return f'[CODE] {text}'

    def block_code(self, text: str, info: str | None) -> str:
        return f'[CODE | {info}] {text}'

    def inline_html(self, _: str) -> str:
        return ''

    def blank_line(self) -> str:
        return ' '

    def softbreak(self) -> str:
        return '\n'

    def paragraph(self, text: str) -> str:
        return text

    def text(self, text: str) -> str:
        return text

    def discord_spoiler(self, text: str) -> str:
        return color(text=text, fg=Colors.BLACK, bg=Colors.BLACK)

    def discord_emoji(self, text: str, emoji_id: int, animated: bool) -> str:
        return f':{text}:'
