# Written by eriaht 08/12/23

import re

# Get valid ip address
def get_valid_ip():
    ip_address = None
    
    while True:
        ip_address = input("Enter ip address: ")
        
        if not re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip_address):
            print('Please enter a valid IPv4 address')
            continue
        else:
            break

    return ip_address