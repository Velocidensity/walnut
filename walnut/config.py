from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import tomllib


@dataclass
class IRCConfig:
    server: str
    port: int
    ssl: bool
    nickname: str
    username: str
    realname: str


@dataclass
class RelayConfig:
    irc_channel: str
    discord_channel_id: int
    discord_webhook: str | None
    colorize_irc_nicknames: bool = True
    use_discord_nicknames: bool = True
    use_discord_usernames_with_nicknames: bool = True
    prevent_self_pinging: bool = True
    expand_emotes: bool = True
    enable_stickers: bool = True


@dataclass
class Config:
    discord_token: str
    irc_config: IRCConfig
    relays: list[RelayConfig]

    @classmethod
    def load(cls, file: Path):
        with file.open(mode='rb') as fp:
            config = tomllib.load(fp)

        for key in ('discord', 'irc'):
            if key not in config.keys():
                raise ValueError(f'"{key}" key missing from config')

        if 'token' not in config['discord'].keys():
            raise ValueError('"token" key missing from the "discord" config section')

        for key in ('server', 'port', 'ssl', 'nickname'):
            if key not in config['discord'].keys():
                raise ValueError(f'"{key}" key missing from the "irc" config section')

        return cls(
            discord_token=config['discord']['token'],
            irc_config=IRCConfig(
                server=config['irc']['server'],
                port=config['irc']['port'],
                ssl=config['irc']['ssl'],
                nickname=config['irc']['nickname'],
                username=config['irc'].get('username', config['irc']['nickname']),
                realname=config['irc'].get('realname', config['irc']['username'])
            ),
            relays=[RelayConfig(**relay) for relay in config['relay']]
        )
