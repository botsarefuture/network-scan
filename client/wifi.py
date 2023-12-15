import pywifi
import time

def get_available_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming you only have one Wi-Fi interface

    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()

    if not scan_results:
        print("No Wi-Fi networks found.")
        return None

    print("Available Wi-Fi networks:")
    for index, result in enumerate(scan_results):
        print(f"{index + 1}. SSID: {result.ssid}, Signal Strength: {result.signal}")

    return scan_results

def get_wifi_info_by_index(index, scan_results):
    if 1 <= index <= len(scan_results):
        selected_network = scan_results[index - 1]
        return selected_network, f"Selected Wi-Fi network: SSID: {selected_network.ssid}, Signal Strength: {selected_network.signal}"
    else:
        return "Invalid index. Please choose a valid Wi-Fi network."

def select_network():
    # Example usage:
    networks = get_available_wifi_networks()

    if networks:
        selected_index = int(input("Enter the index of the Wi-Fi network you want more information about: "))
        selected_network, info = get_wifi_info_by_index(selected_index, networks)
        print(info)
        
        return selected_network.ssid
