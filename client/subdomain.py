import socket
from tqdm import tqdm

def scan_subdomains_function(domain, gui=False):
    subdomains = []

    if gui:
        print("WELCOME TO SUBDOMAIN SCANNER!\nSelect one of the modes below:")
        print("[1] Most common subdomains (718 pcs)")
        print("[2] 100 most common subdomains")
        print("[3] 500 most common subdomains")
        print("[4] 1000 most common subdomains")
        print("[5] 10000 most common subdomains")

        try:
            select = int(input("Select now:  "))
            options = [1, 2, 3, 4, 5]
            if select not in options:
                raise ValueError("Invalid selection. Using most common 718 subdomains for now. Press ctrl+C to abort.")
        except ValueError as ve:
            print(f"Error: {ve}")
            select = 1

        file_mapping = {1: 'common.txt', 2: '100.txt', 3: '500.txt', 4: '1000.txt', 5: '10000.txt'}
        file = file_mapping.get(select, 'common.txt')

        with open(f"subdomains/{file}", 'r') as f:
            subdomains_to_scan = f.readlines()
    else:
        with open("subdomains/common.txt", "r") as f:
            subdomains_to_scan = f.readlines()

    try:
        ip_address = socket.gethostbyname(domain)
        total_subdomains = len(subdomains_to_scan)

        for subdomain in tqdm(subdomains_to_scan, desc="Scanning Subdomains", unit="subdomain"):
            subdomain = subdomain.strip()
            subdomain_full = f"{subdomain}.{domain}"
            try:
                subdomain_ip = socket.gethostbyname(subdomain_full)
                subdomain_data = {"ip": subdomain_ip, "name": subdomain_full}
                subdomains.append(subdomain_data)
            except socket.error:
                pass

    except socket.error as e:
        print(f"Error: {e}")

    print("\nScan complete.")
    return subdomains

def scan_subdomains():
    domain = input("Enter domain to scan: ")
    try:
        result = scan_subdomains_function(domain, True)
        print(f"\nScan result for domain {domain}")
        print("--------------------------------")
        for subdomain_data in result:
            print(subdomain_data)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#scan_subdomains()
