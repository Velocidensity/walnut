Configuration
==================================

------------------------------
Connection
------------------------------

This section must be filled out fully (excluding optional fields).

.. code-block:: toml

   [discord]
   # Discord bot token.
   token = ""

   [irc]
   # Server hostname/IP
   server = "irc.example.com"
   # Server port, typically 6697 (SSL) or 6667 (plaintext).
   port = 6697
   # Connect using SSL
   ssl = true
   # Nickname
   nickname = "Walnut"
   # (Optional) Username, if ommitted, nickname will be used
   username = "Walnut"
   # (Optional) Realname, if ommitted, nickname will be used
   realname = "Walnut"
   # (Optional) Server password, typically unused unless using ZNC
   password = null

To obtain a Discord bot token, follow discord.py's documentation on `bot creation`_.

.. _bot creation: https://discordpy.readthedocs.io/en/latest/discord.html

------------------------------
Relays
------------------------------

This section can be repeated for as many channel pairs as desired, or ommitted entirely, if using a custom hook.

.. code-block:: toml

   [[relay]]
   # IRC channel name
   irc_channel = "#channel-name"
   # Discord channel ID
   discord_channel_id = 1111111
   # (Optional) Discord webhook URL
   discord_webhook_url = "https://discord.com/api/webhooks/1111111111111111111/web_hook_stuff"
   # Assign a color to every Discord nickname sent on IRC
   # Use Discord's display names instead of usernames
   colorize_irc_nicknames = true
   use_discord_nicknames = true
   # Show Discord usernames next to display names
   use_discord_usernames_with_nicknames = true
   # Prevent pinging Discord members on IRC by inserting a zero-width space
   prevent_self_pinging = true
   # Enable sending Discord stickers on IRC (name and image)
   enable_stickers = true

To find a Discord channel ID, see "`Where can I find my User/Server/Message ID?`_".

Using a Discord webhook is strongly recommended, as it allows for matching usernames/avatars of Discord members. See "`Intro to Webhooks`_" for instructions on creating one.

.. _Where can I find my User/Server/Message ID?: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-
.. _Intro to Webhooks: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
