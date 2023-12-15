from menu import display_menu
from ddos import perform_ddos_attack_wrapper
from port_scan import port_scan
from subdomain import scan_subdomains

title = """
.##.....##.########.########..########
.##.....##.##.......##.....##......##.
.##.....##.##.......##.....##.....##..
.##.....##.######...########.....##...
..##...##..##.......##...##.....##....
...##.##...##.......##....##...##.....
....###....########.##.....##.########
"""

print(title)
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

if __name__ == "__main__":
    valikko()
