import requests
import time
import sys

# --- USER CONFIG ---
authToken = ""
userId = ""
serverId = ""
# -------------------

batchCount = 0
msgCount = 0


def load_user():
    r = requests.get("https://discordapp.com/api/v6/users/@me",
                     headers={"Authorization": authToken})
    response = r.json()
    username = response["username"]
    discriminator = response["discriminator"]
    return [username, discriminator]


def load_messages():
    r = requests.get("https://discordapp.com/api/v6/guilds/" + str(serverId) +
                     "/messages/search?author_id=" + str(userId),
                     headers={"Authorization": authToken})

    if r.status_code == 200:
        pass
    elif r.status_code == 429:
        pass
    response = r.json()
    if response["total_results"] == 0:
        return None
    else:
        return response


def delete_message(message):
    r = requests.delete("https://discordapp.com/api/v6/channels/" +
                        message["channel_id"] + "/messages/" + message["id"],
                        headers={"Authorization": authToken})
    if r.status_code == 204:
        global msgCount
        msgCount += 1


def loading_output(mode, bc=0, mc=0):
    if mode == "w":
        msg = "[i] Deleting messages{:5s} [batch #{}]".format("." * (mc % 5), bc)
    elif mode == "x":
        msg = "[!] Finished deleting {} messages!          ".format(mc)
    return msg


def main():
    loadedMessages = load_messages()
    global batchCount
    batchCount += 1
    if loadedMessages is None:
        print("\r" + loading_output("x", mc=msgCount), end="", flush=True)
        return
    for batch in loadedMessages["messages"]:
        for msg in batch:
            if msg["author"]["id"] == userId:
                delete_message(msg)
                print("\r" + loading_output("w",
                                            bc=batchCount, mc=msgCount), end="")
    main()


if __name__ == "__main__":
    try:
        print("""
     ___                     __  
 ___/ (_)__ _______  _______/ /  
/ _  / (_-</ __/ _ \/ __/ _  /   
\_,_/_/___/\__/\___/_/  \_,_/    
              __    __    __     
          ___/ /__ / /__ / /____ 
         / _  / -_) / -_) __/ -_)
         \_,_/\__/_/\__/\__/\__/                           
""")    
        info = load_user()
        print(("[i] User >> {}#{} <<").format(info[0], info[1]))
        main()
    except KeyboardInterrupt:
        print("\n[!] Shutting down...", end="")
        time.sleep(2)
        sys.exit()
    load_user()
