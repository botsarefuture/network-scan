import re
import requests
from bs4 import BeautifulSoup

from datetime import datetime

link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'

time = int(datetime.now().timestamp())

payload = {
    'username': 'vuoreol',
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:shohp8sa',  # <-- note the '0' - that means we want to use plain passwords
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
print(r.url)
print(r.text)

data = r.json()

if data["authenticated"]:
    print("Success")        