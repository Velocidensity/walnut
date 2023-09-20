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
- custom Discord commands must be synced manually

# Documentation
https://velocidensity.github.io/walnut/

Refer to the documentation for installation, usage and extending instructions.

# Disclaimer
Featureset of this project is tailored specifically for my needs, and feature requests will likely not be accepted. If all you need is a simple bridge, you may be better off using something else, like [matterbridge](https://github.com/42wim/matterbridge) or [discord-irc](https://github.com/reactiflux/discord-irc).

# Credits, acknowledgements
IRC formatting constants were taken from [sopel](https://github.com/sopel-irc/sopel), licensed under Eiffel Forum License, version 2, and modified for the purposes of this project.

This project was made possible by excellent libraries handling the underlying connections, [discord.py](https://github.com/Rapptz/discord.py) and [pyrcb2](https://github.com/taylordotfish/pyrcb2).

Some features were inspired by [discord-irc](https://github.com/reactiflux/discord-irc) and [matterbridge](https://github.com/42wim/matterbridge).
