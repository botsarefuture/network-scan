import socket

from tqdm import tqdm


# Dictionary containing information about common ports
ports = {
    20: {"name": "FTP Data", "short_name": "FTP-DATA"},
    21: {"name": "FTP Control", "short_name": "FTP"},
    22: {"name": "SSH (Secure Shell)", "short_name": "SSH"},
    23: {"name": "TELNET", "short_name": "TELNET"},
    25: {"name": "SMTP (Simple Mail Transfer Protocol)", "short_name": "SMTP"},
    53: {"name": "DNS (Domain Name System)", "short_name": "DNS"},
    67: {"name": "DHCP (Dynamic Host Configuration Protocol)", "short_name": "DHCP"},
    68: {"name": "DHCP (Dynamic Host Configuration Protocol)", "short_name": "DHCP"},
    69: {"name": "TFTP (Trivial File Transfer Protocol)", "short_name": "TFTP"},
    80: {"name": "HTTP", "short_name": "HTTP"},
    110: {"name": "POP3 (Post Office Protocol version 3)", "short_name": "POP3"},
    115: {"name": "SFTP (Simple File Transfer Protocol)", "short_name": "SFTP"},
    119: {"name": "NNTP (Network News Transfer Protocol)", "short_name": "NNTP"},
    123: {"name": "NTP (Network Time Protocol)", "short_name": "NTP"},
    135: {"name": "MS RPC (Microsoft Remote Procedure Call Protocol)", "short_name": "MS-RPC"},
    137: {"name": "NetBIOS Name Service", "short_name": "NETBIOS-NS"},
    138: {"name": "NetBIOS Datagram Service", "short_name": "NETBIOS-DGM"},
    139: {"name": "NetBIOS Session Service", "short_name": "NETBIOS-SSN"},
    143: {"name": "IMAP4 (Internet Message Access Protocol version 4)", "short_name": "IMAP"},
    161: {"name": "SNMP (Simple Network Management Protocol)", "short_name": "SNMP"},
    162: {"name": "SNMP Trap", "short_name": "SNMP-TRAP"},
    179: {"name": "BGP (Border Gateway Protocol)", "short_name": "BGP"},
    194: {"name": "IRC (Internet Relay Chat)", "short_name": "IRC"},
    389: {"name": "LDAP (Lightweight Directory Access Protocol)", "short_name": "LDAP"},
    443: {"name": "HTTPS (Hypertext Transfer Protocol Secure)", "short_name": "HTTPS"},
    445: {"name": "Microsoft-DS (Microsoft Directory Services)", "short_name": "MICROSOFT-DS"},
    465: {"name": "SMTPS (SMTP Secure)", "short_name": "SMTPS"},
    514: {"name": "Syslog", "short_name": "SYSLOG"},
    587: {"name": "SMTP (Submission)", "short_name": "SUBMISSION"},
    636: {"name": "LDAPS (LDAP Secure)", "short_name": "LDAPS"},
    993: {"name": "IMAPS (IMAP over TLS/SSL)", "short_name": "IMAPS"},
    995: {"name": "POP3S (POP3 over TLS/SSL)", "short_name": "POP3S"},
    1080: {"name": "SOCKS Proxy", "short_name": "SOCKS"},
    1433: {"name": "Microsoft SQL Server", "short_name": "MSSQL"},
    1521: {"name": "Oracle Database", "short_name": "ORACLE"},
    3306: {"name": "MySQL Database", "short_name": "MYSQL"},
    3389: {"name": "RDP (Remote Desktop Protocol)", "short_name": "RDP"},
    5432: {"name": "PostgreSQL", "short_name": "POSTGRES"},
    5900: {"name": "VNC (Virtual Network Computing)", "short_name": "VNC"},
    8080: {"name": "HTTP Alternative", "short_name": "HTTP-ALT"},
    8443: {"name": "HTTPS Alternative", "short_name": "HTTPS-ALT"}}

def perform_port_scan_function(ip, start_port, end_port):    
    print(f"[!] Now scanning {ip}")
    open_ports = []

    total_ports = end_port - start_port + 1

    
    # Loop through the specified port range
    for port in tqdm(range(start_port, end_port + 1), desc=f"Scanning {ip}", unit="port"):
        try:
            # Attempt to create a connection to the IP and port
            with socket.create_connection((ip, port), timeout=1) as sock:
                print(f"[+] {port} {ports.get(port, {}).get('short_name', '').upper()}")
                open_ports.append(port)
        except socket.error as e:
            if str(e) == "timed out":
                continue
            print(f"Error scanning port {port}: {e}")

    print("\nScan complete.")
    return {"open_ports": open_ports}

def port_scan():
    try:
        # Get input from the user
        target_ip = input("Enter target IP address: ")
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
    except ValueError:
        print("Invalid port numbers. Please enter valid integers.")
        return

    results = perform_port_scan_function(target_ip, start_port, end_port)

    print(f"Port scan results for {target_ip} (ports {start_port}-{end_port})")
    print("--------------------------------")

    print(results["open_ports"])