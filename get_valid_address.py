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

# Get valid ip address
def get_valid_subnet_mask():
    mask = None
    
    while True:
        mask = input("Enter subnet mask: ")
        
        if not re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", mask):
            print('Please enter a valid subnet mask')
            continue

        mask_octets = [int(octet) for octet in mask.split('.')]

        significant_octet_index = None
        for index, octect in enumerate(mask_octets):
            if octect in range(1, 255):
                significant_octet_index = index
                break
        
        error_in_mask = False
        for index in range(significant_octet_index + 1, len(mask_octets)):
            if mask_octets[index] != 0:
                error_in_mask = True
                break
        
        if error_in_mask: 
            print('Please enter a valid subnet mask') 
            continue

        if significant_octet_index:
            if mask_octets[significant_octet_index] not in [128, 192, 224, 240, 248, 252, 254]:
                print('Please enter a valid subnet mask')
                continue
        else:
            break
        
    return mask