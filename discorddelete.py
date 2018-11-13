import sys
import time


# --- USER CONFIG ---
authToken = ""
userId = ""
serverId = ""
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
        print(Fore.RED +
              "\r[x] Authorization failed",
              end="")
        print(Fore.RED +
              "\n[x] Possibly invalid 'authToken' provided",
              end="")
        exit()


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


def loading_output(bc=0, mc=0):
    msg = "[-] Deleting messages{:5s} [batch #{}]".format(
        "." * (mc % 5), bc)
    return msg


def main():
    loadedMessages = load_messages()
    global batchCount
    batchCount += 1
    if loadedMessages is None:
        print(Fore.GREEN +
              "\r[!] Finished deleting {} messages!          ".format(
                  msgCount), end="", flush=True)
        exit()
    if loadedMessages is False:
        timeout = rDelay % 120
        for t in range(timeout, -1, -1):
            if t > 0:
                print(
                    (Fore.RED + "\r[x] Discord API timeout (retry in {}s)   ")
                    .format(t), end="", flush=True)
                time.sleep(1)
            else:
                print(Fore.RED +
                      "\r[x] Discord API timeout (retrying...)   ",
                      end="", flush=True)
                time.sleep(1)
        main()
    for batch in loadedMessages["messages"]:
        for msg in batch:
            if msg["author"]["id"] == userId:
                delete_message(msg)
                print("\r" + loading_output(bc=batchCount, mc=msgCount),
                      end="")
    main()


def exit():
    print(Fore.LIGHTBLACK_EX + "\n[!] Press any key to exit...", end="")
    input()
    sys.exit()


def shutdown(t):
    print(Fore.LIGHTBLACK_EX + "\n[!] Shutting down...", end="")
    time.sleep(t)
    sys.exit()


if __name__ == "__main__":
    try:
        import requests
        from colorama import init, Fore, Back, Style
        init()
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
        shutdown(3)
    except requests.exceptions.Timeout:
        print(Fore.RED + "\r[x] Network connection timeout", end="")
        exit()
    except requests.exceptions.ConnectionError:
        print(
            Fore.RED + "\r[x] Network connectivity limited or unavailable",
            end="")
        exit()
    except requests.exceptions.RequestException:
        print(Fore.RED + "\r[x] Unexpected error occured", end="")
        exit()
    except (ImportError, ModuleNotFoundError, NameError):
        print("\r[x] Missing packages 'colorama' or 'requests'", end="")
        print("\n[x] Type 'pip install colorama requests' to install", end="")
        print("\n[!] Press any key to exit...", end="")
    input()
    sys.exit()
