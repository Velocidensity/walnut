# Walnut
An extensible hybrid Discord/IRC bot. **WIP**

# Relay features
- message relaying between Discord/IRC
- (IRC) colored nicknames
- (IRC) avoiding pinging users present on both channels
- (IRC) showing server name, global name or both
- (IRC) showing emote name, URL or both
- (IRC) sticker support (name or URL)
- (IRC) replies support
- (Discord) using web hooks for message
- (Discord) matching user avatars if possible

# Limitations
- only one IRC server and one Discord account are currently supported

# Setup
Bot must have message content and server members privileged intents enabled.

# Disclaimer
Featureset of this project is tailored specifically for my needs, and feature requests will likely not be accepted. You may be better off using something else, like [matterbridge](https://github.com/42wim/matterbridge).

# Acknowledgements
IRC formatting constants were taken from [sopel](https://github.com/sopel-irc/sopel), licensed under Eiffel Forum License, version 2, and modified for the purposes of this project.

This project heavily relies on [discord.py](https://github.com/Rapptz/discord.py) and [pyrcb2](https://github.com/taylordotfish/pyrcb2).

Some features were inspired by [discord-irc](https://github.com/reactiflux/discord-irc) and [matterbridge](https://github.com/42wim/matterbridge).
