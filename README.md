# discorddelete

Simple script to delete all messages sent in a specific server.

## How to run

1. Get your user and server id

2. Get your authorization token
    * Go to https://discordapp.com/app
    * Open the dev tools (F12), open the Network tab. (You should clear all requests for better readability if you see some.)
    * Delete one message manually. In the request log, you will see a request with a `DELETE` method.
    * Click on the request to open the details, and on the Headers tab, copy the 'authorization' token.

## TODO
