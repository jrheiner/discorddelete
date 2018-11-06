import requests
import time
import sys

# --- USER CONFIG ---
authToken = ""
userId = ""
serverId = ""
# If you are not sure how to get user and server id check:
# https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-
# -------------------

batchCount = 0
msgCount = 0
global rDelay
rDelay = 0


def load_user():
    r = requests.get("https://discordapp.com/api/v6/users/@me",
                     headers={"Authorization": authToken}, timeout=15)
    response = r.json()
    try:
        username = response["username"]
        discriminator = response["discriminator"]
        return [username, discriminator]
    except KeyError:
        print(
            "\r[x] Authorization failed",
            end="")
        print(
            "\n[x] Possibly invalid 'authToken' provided",
            end="")
        print("\n[!] Shutting down...", end="")
        time.sleep(5)
        sys.exit()


def load_messages():
    r = requests.get("https://discordapp.com/api/v6/guilds/" + str(serverId) +
                     "/messages/search?author_id=" + str(userId),
                     headers={"Authorization": authToken})

    if r.status_code == 200:
        pass
    elif r.status_code == 429:
        global rDelay
        rDelay += 5
        return False
    else:
        return False
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
        msg = "[-] Deleting messages{:5s} [batch #{}]".format(
            "." * (mc % 5), bc)
    elif mode == "x":
        msg = "[!] Finished deleting {} messages!          ".format(mc)
    return msg


def main():
    loadedMessages = load_messages()
    global batchCount
    batchCount += 1
    if loadedMessages is None:
        print("\r" + loading_output("x", mc=msgCount), end="", flush=True)
        print("\n[!] Press any key to exit...", end="")
        input()
        sys.exit()
    if loadedMessages is False:
        timeout = rDelay % 120
        for t in range(timeout, -1, -1):
            if t > 0:
                print(
                    ("\r" + "[x] Discord API timeout (retry in {}s)   ")
                    .format(t), end="", flush=True)
                time.sleep(1)
            else:
                print(
                    "\r" + "[x] Discord API timeout (retrying...)   ",
                    end="", flush=True)
                time.sleep(1)
        main()
    for batch in loadedMessages["messages"]:
        for msg in batch:
            if msg["author"]["id"] == userId:
                delete_message(msg)
                print("\r" + loading_output("w",
                                            bc=batchCount, mc=msgCount),
                      end="")
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
        print(("[+] User >> {}#{}").format(info[0], info[1]))
        main()
    except KeyboardInterrupt:
        print("\n[!] Shutting down...", end="")
        time.sleep(3)
        sys.exit()
    except requests.exceptions.Timeout:
        print("\r[x] Network connection timeout", end="")
        print("\n[!] Shutting down...", end="")
        time.sleep(5)
        sys.exit()
    except requests.exceptions.ConnectionError:
        print("\r[x] Network connectivity limited or unavailable", end="")
        print("\n[!] Shutting down...", end="")
        time.sleep(5)
        sys.exit()
    except requests.exceptions.RequestException:
        print("\r[x] Unexpected error occured", end="")
        print("\n[!] Shutting down...", end="")
        time.sleep(5)
        sys.exit()

