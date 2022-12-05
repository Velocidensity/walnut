from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import tomllib
from pyrcb2.itypes import IStr


@dataclass
class IRCConfig:
    """Class storing IRC connection configuration"""
    server: str
    port: int
    ssl: bool
    nickname: str
    username: str
    realname: str
    password: str | None = None


@dataclass
class RelayConfig:
    """Class storing Discord/IRC relay configuration"""
    irc_channel: IStr
    discord_channel_id: int
    discord_webhook_url: str | None
    colorize_irc_nicknames: bool = True
    use_discord_nicknames: bool = True
    use_discord_usernames_with_nicknames: bool = True
    prevent_self_pinging: bool = True
    expand_emotes: bool = True
    enable_stickers: bool = True


@dataclass
class Config:
    """Class storing Walnut configuration"""
    discord_token: str
    irc_config: IRCConfig
    relays: list[RelayConfig]

    @classmethod
    def from_file(cls, file: Path) -> Config:
        with file.open(mode='rb') as fp:
            config = tomllib.load(fp)

        for key in ('discord', 'irc'):
            if key not in config.keys():
                raise ValueError(f'"{key}" key missing from config')

        if 'token' not in config['discord'].keys():
            raise ValueError('"token" key missing from the "discord" config section')

        for key in ('server', 'port', 'ssl', 'nickname'):
            if key not in config['irc'].keys():
                raise ValueError(f'"{key}" key missing from the "irc" config section')

        return cls(
            discord_token=config['discord']['token'],
            irc_config=IRCConfig(
                server=config['irc']['server'],
                port=config['irc']['port'],
                ssl=config['irc']['ssl'],
                nickname=config['irc']['nickname'],
                username=config['irc'].get('username', config['irc']['nickname']),
                realname=config['irc'].get('realname', config['irc']['nickname']),
                password=config['irc'].get('password')
            ),
            relays=[RelayConfig(**relay) for relay in config['relay']]
        )
