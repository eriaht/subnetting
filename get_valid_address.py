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

        if len(set(mask_octets)) == 1 and list(set(mask_octets))[0] == 255:
            break

        significant_octet_index = -1
        for index, octect in enumerate(mask_octets):

            if index != len(mask_octets) - 1:
                if octect == 255 and (mask_octets[index + 1] == 0):
                    significant_octet_index = index
                    break

            if octect in range(1, 255):
                significant_octet_index = index
                break
        
        error_in_mask = False
        if significant_octet_index > -1 and (significant_octet_index != len(mask_octets) - 1):
            for index in range(significant_octet_index + 1, len(mask_octets)):
                if mask_octets[index] != 0:
                    error_in_mask = True
                    break

        if error_in_mask: 
            print('Please enter a valid subnet mask') 
            continue

        if significant_octet_index > -1:
            if mask_octets[significant_octet_index] not in [128, 192, 224, 240, 248, 252, 254, 255]:
                print('Please enter a valid subnet mask')
                continue
            else:
                break
        
    return mask