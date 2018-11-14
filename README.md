# discorddelete.py

Script to delete all messages of a user sent in a specific server.

## How to run

1. Get your user and server id
    * [How to find user and server id](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

2. Get your authorization token (**DO NOT SHARE IT**)
    * Go to the [discord webclient](https://discordapp.com/channels/@me) and sign in

    * Type `javascript:` in the URL bar and copy the following

        ```js
        prompt("Your discord authToken", document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token.replace(/"/g, ""));
        ```


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

* [Python Package `requests`](https://pypi.org/project/requests/)

    > pip install colorama requests
