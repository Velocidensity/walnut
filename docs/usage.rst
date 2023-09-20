Installation and setup
==================================

------------------------------
Installation
------------------------------

.. code-block:: console

   $ pip install git+https://github.com/Velocidensity/walnut

Optionally with a virtual environment of your choice.

------------------------------
Setup
------------------------------

#. Create a Discord bot, with message content and server members privileged intents enabled.

   For more information on this, see discord.py's documentation on `bot creation`_ and `intents`_.

   .. _bot creation: https://discordpy.readthedocs.io/en/latest/discord.html
   .. _intents: https://discordpy.readthedocs.io/en/latest/intents.html


#. Generate a configuration file using:

   .. code-block:: console

      $ walnut config

#. Fill out the configuration file. See :doc:`configuration` for instructions.
#. Start the bot with:

   .. code-block:: console

      $ walnut run
