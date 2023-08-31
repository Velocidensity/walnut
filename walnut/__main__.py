import shutil
import sys
from pathlib import Path

import click

from walnut.bot import WalnutBot
from walnut.config import Config
from walnut.hooks.relay import MessageRelay

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option(
    '-c', '--config', 'config_file',
    default=Path('config.toml'),
    type=Path,
    help='Configuration file'
)
def run(config_file: Path) -> None:
    """Starts the bot with configured relays"""
    config = Config.from_file(config_file)
    bot = WalnutBot(config)
    for relay_config in config.relays:
        MessageRelay.from_config(relay_config).load(bot)

    bot.run()


@cli.command()
@click.option(
    '-c', '--config', 'config_file',
    default=Path('config.toml'),
    type=Path,
    help='Configuration file'
)
def config(config_file: Path) -> None:
    """Generates an example config"""
    example_path = Path(__file__).parent / '_data' / 'config.toml.example'
    if not example_path.exists():
        raise RuntimeError('Example config file could not be found')

    if config_file.exists():
        print('Configuration file exists, not overwriting.')
        sys.exit(1)

    shutil.copy(example_path, config_file)
    print(f'Done! Example configuration file saved to {config_file}')


if __name__ == "__main__":
    cli()
