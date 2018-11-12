# discorddelete.py

Script to delete all messages of a user sent in a specific server.

## How to run

1. Get your user and server id
    * [How to find user and server id](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

2. Get your authorization token
    * [How to find your authorization token](https://discordhelp.net/discord-token)
    * **DO NOT SHARE IT**

3. Fill out the user config at the top the script

   ```python
   # --- USER CONFIG ---
   authToken = ""
   userId = ""
   serverId = ""
   # -------------------
   ```

4. To start the script type `python discorddelete.py`

### Requirements

* [Python 3.6+](https://www.python.org/downloads/)

* [Python Package `colorama`](https://pypi.org/project/colorama/)
    > pip install colorama

## TODO

* implement [bulk-delete-messages](https://discordapp.com/developers/docs/resources/channel#bulk-delete-messages) to delete most recent messages instead of using single requests

* add indicator of messages left or progessbar of deleted messages/total messages
