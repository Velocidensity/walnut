# Walnut
An extensible hybrid Discord/IRC relay bot.

# Relay features
|                     | IRC -> Discord | Discord -> IRC                                         |
|---------------------|----------------|--------------------------------------------------------|
| Custom nicknames    | ❌             | ✔️                                                     |
| Matching avatars    | ✔️             | ❌                                                     |
| Colored nicknames   | ❌             | ✔️ (nickname colors have no relation to Discord roles) |
| Unicode emojis      | ✔️             | ✔️                                                     |
| Custom emojis       | ❌             | ✔️ (name/URL)                                          |
| Replies             | ❌             | ✔️ (nickname only)                                     |
| Stickers            | ❌             | ✔️ (name/URL)                                          |
| Prevent double ping | ✔️             | ✔️                                                     |

# Limitations
- only one IRC server and one Discord account are currently supported
- custom messsage templates are currently not supported

# Setup
Bot must have message content and server members privileged intents enabled.
Generate a config with `walnut config`, fill it out, and start with `walnut run`.

# Extending
Sublcassing `walnut.hooks.base.BaseHook` or `walnut.hooks.relay.MessageRelay` will be the easiest option. Alternatively, you can attach any method taking a `walnut.irc.message.Message`/`discord.Message` object to `walnut.bot.WalnutBot.irc_hooks`/`walnut.bot.WalnutBot.discord_hooks`.

`WalnutBot` implements a `discord.app_commands.CommandTree` and has a `add_discord_command` method, which can be used to add custom commands. Syncing has to be done manually after `run()` is called (or at least `WalnutBot.discord` is started).

# Disclaimer
Featureset of this project is tailored specifically for my needs, and feature requests will likely not be accepted. You may be better off using something else, like [matterbridge](https://github.com/42wim/matterbridge).

# Credits, acknowledgements
IRC formatting constants were taken from [sopel](https://github.com/sopel-irc/sopel), licensed under Eiffel Forum License, version 2, and modified for the purposes of this project.

This project was made possible by excellent libraries handling the underlying connections, [discord.py](https://github.com/Rapptz/discord.py) and [pyrcb2](https://github.com/taylordotfish/pyrcb2).

Some features were inspired by [discord-irc](https://github.com/reactiflux/discord-irc) and [matterbridge](https://github.com/42wim/matterbridge).
