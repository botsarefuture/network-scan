import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import nmap
import socket

BASE_URL = 'http://clienturl:5000'
PORT_RANGE = '1-65535'

logging.basicConfig(level=logging.INFO)

from datetime import datetime
import pytz

def get_current_time():
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)
    
    return str(utc_now)

def submit_results(results):
    data = {"results": results, "time": get_current_time()}
    requests.post(f'{BASE_URL}/submit_results', json=data)

def scan_ip(ip):
    try:
        nm = nmap.PortScanner()
        nm._nmap_opt = '-Pn'
        common_ports = [21, 22, 80, 443, 8080]
        common_scan_args = '-p {}'.format(','.join(map(str, common_ports)))
        nm.scan(ip, arguments=common_scan_args)

        open_common_ports = [port for port in common_ports if nm[ip]['tcp'][port]['state'] == 'open']

        if open_common_ports:
            logging.info(f"Common ports open on {ip}: {open_common_ports}")
        else:
            logging.info(f"No common ports open on {ip}")
            nm.scan(ip, arguments=f'-p 0-65535')

        open_ports = [port for port in nm[ip]['tcp'] if nm[ip]['tcp'][port]['state'] == 'open']
        logging.info(f"All open ports on {ip}: {open_ports}")

        if 80 in nm[ip]['tcp']:
            webpage_url = f'http://{ip}'
            webpage_data = scan_webpage(webpage_url)
        else:
            webpage_data = None

        return {"ip": ip, "open_ports": open_ports, "webpage_data": webpage_data, "error": None}

    except KeyError as e:
        logging.error(f"Error scanning {ip}: {e}")
        return {"ip": ip, "open_ports": None, "webpage_data": None, "error": str(e)}


    
    except nmap.nmap.PortScannerError as e:
        logging.error(f"Error scanning {ip}: {e}")
        return {"ip": ip, "open_ports": None, "webpage_data": None, "error": str(e)}

def scan_webpage(webpage_url):
    try:
        response = requests.get(webpage_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        internal_links = extract_internal_links(webpage_url, soup)

        logging.info(f"Internal links on {webpage_url}: {internal_links}")

        return {"webpage_url": webpage_url, "internal_links": internal_links, "error": None}

    except Exception as e:
        logging.error(f"Error while scanning {webpage_url}: {e}")
        return {"webpage_url": webpage_url, "internal_links": None, "error": str(e)}

def extract_internal_links(base_url, soup):
    internal_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            internal_links.append(full_url)
    return internal_links

def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

def main():
    while True:
        while not is_internet_available():
            logging.warning("No internet connection. Retrying in 10 seconds...")
            time.sleep(10)

        data = requests.get(f'{BASE_URL}/get_ip').json()
        if data.get("ip"):
            logging.info(data.get("ip"))
            results = scan_ip(data.get("ip"))
            submit_results(results)
        else:
            logging.error(data.get("error"))

        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
