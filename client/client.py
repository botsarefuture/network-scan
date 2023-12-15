from menu import display_menu
from ddos import perform_ddos_attack_wrapper
from port_scan import port_scan
from subdomain import scan_subdomains
from brute import main as brute_main

TITLE = """
.##.....##.########.########..########
.##.....##.##.......##.....##......##.
.##.....##.##.......##.....##.....##..
.##.....##.######...########.....##...
..##...##..##.......##...##.....##....
...##.##...##.......##....##...##.....
....###....########.##.....##.########
"""

def menu():
    while True:
        display_menu()
        choice = input("Select function (q to quit): ")

        if choice == '0':
            perform_ddos_attack_wrapper()
        elif choice == '1':
            port_scan()
        elif choice == '2':
            brute_main()
        elif choice == '3':
            scan_subdomains()
        elif choice.lower() == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    print(TITLE)
    menu()
