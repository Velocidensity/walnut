Extending
==================================

------------------------------
Creating a custom hook class
------------------------------

To create a custom hook, subclass :py:class:`~walnut.hooks.base.BaseHook` and implement the following methods.

* :py:meth:`~walnut.hooks.base.BaseHook.handle_discord_message`
    This will be called on every incoming Discord message.

    Can be left as a noop, if this is an IRC only hook.

* :py:meth:`~walnut.hooks.base.BaseHook.handle_irc_message`
    This will be called on every incoming IRC message.

    Can be left as a noop, if this is a Discord only hook.

* :py:meth:`~walnut.hooks.base.BaseHook.load`
    This method should load the hook into a :py:class:`~walnut.bot.WalnutBot` instance.

    At a minimum, it should add message handling methods to
    :py:attr:`~walnut.bot.WalnutBot.discord_hooks` and :py:attr:`~walnut.bot.WalnutBot.irc_hooks` respectively.


------------------------------
Loading a custom hook class
------------------------------

To load a custom hook, you will need to create a :py:class:`~walnut.bot.WalnutBot` instance directly,
provide it with an appropriate :py:class:`~walnut.config.Config`, and call :py:meth:`~walnut.bot.WalnutBot.run` manually,
bypassing the CLI interface. To provide custom configuration options for your hook, you might need to subclass :py:class:`~walnut.config.Config`.


------------------------------
Manual hooks
------------------------------

Any method with compatible parameters can be added to :py:attr:`~walnut.bot.WalnutBot.discord_hooks` and :py:attr:`~walnut.bot.WalnutBot.irc_hooks`.
This allows use of entirely separate classes, and standalone functions.

------------------------------
Discord commands
------------------------------

To add a Discord command, create an appropriate object, and pass it to :py:meth:`~walnut.bot.WalnutBot.add_discord_command`.

Refer to documentation for `discord.ext.commands`_ and `discord.py's examples`_ for more instructions.

Syncing currently has to be done manually after :py:meth:`~walnut.bot.WalnutBot.run` is called (or at least :py:attr:`~walnut.bot.WalnutBot.discord` is started).


.. _discord.ext.commands: https://discordpy.readthedocs.io/en/latest/ext/commands/index.html
.. _discord.py's examples: https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py

