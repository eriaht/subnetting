# Written by eriaht 08/12/23

import re
from argparse import ArgumentParser

# Create a list of containing each octet as an int
def ip_octets_int(ip: str) -> list:
    return [int(octet) for octet in ip.split('.')]

# Convert IP to binary
def ip_to_bin(ip: str) -> list:
    octets_dec = ip_octets_int(ip)
    octets_bin = [f"{bin(octect).replace('0b', ''):>08}" for octect in octets_dec]
    
    return octets_bin

# Determine the IP address class
def ip_class(ip: str) -> str:
    first_octet = ip_octets_int(ip)[0]

    if first_octet in range(1, 128):
        return 'A'
    elif first_octet in range(128, 192):
        return 'B'
    elif first_octet in range(192, 224):
        return 'C'
    elif first_octet in range(224, 240):
        return 'D'
    elif first_octet in range(240, 255):
        return 'E'

# Find network address
def ip_net_id(ip: str, mask: str) -> list:
    ip_octets = ip_octets_int(ip)
    mask_octets = ip_octets_int(mask)
    net_id = []

    for i in range(len(ip_octets)):
        net_id.append(ip_octets[i] & mask_octets[i])

    return net_id

def cidr_32(mask: str) -> bool:
    mask_octets = [int(octet) for octet in mask.split('.')]

    if len(set(mask_octets)) == 1 and list(set(mask_octets))[0] == 255:
        return True
    
    return False

# Find broadcast address
def ip_broadcast(ip: str, mask: str) -> list:
    if cidr_32(mask):
        return ip_octets_int(ip)

    net_id = ip_net_id(ip, mask)
    mask_octets = ip_octets_int(mask)
    broadcast_addr = []

    for i, mask_octet in enumerate(mask_octets):
        if mask_octet == 255:
            broadcast_addr.append(net_id[i])
        elif mask_octet < 255:
            if net_id[i] > 0:
                '''
                Logic for this part
                --------------------
                1. Find the SO (significant octet) for both the network address and subnet mask.
                2. Perform an OR operation between the SO of the network address and the SO of the subnet mask.
                3. Perform an XOR on the output of the above OR operation with 255 or 1111 1111.
                4. Add the SO from the network address to the output of the above operation.

                IP:          137.72.145.170
                Net address: 137.72.144.0
                                     ^-- Significant octet of the network address
                Subnet Mask: 255.255.248.0
                                     ^-- Significant octet of the subnet mask
                
                    10010000 = 144
                or  11111000 = 248
                    ---------------
                    11111000 = 248
                xor 11111111 = 255
                    ---------------
                    00000111 = 7
                +   10010000 = 144
                    ---------------
                    10010111 = 151
                '''
                broadcast_addr.append(((net_id[i] | mask_octets[i]) ^ 255) + net_id[i])
            else:
                broadcast_addr.append((net_id[i] | mask_octets[i]) ^ 255)

    return broadcast_addr

# Find first and last host addresses
def ip_first_last_host(ip:str, net_id: list, broadcast: list) -> tuple:
    first_host = None
    last_host = None
    if ip_octets_int(ip) == broadcast:
        return (ip_octets_int(ip), '')

    first_host = net_id[0:len(net_id) - 1]
    first_host.append(net_id[len(net_id) - 1] + 1)

    last_host = broadcast[0:len(broadcast) - 1]
    last_host.append(broadcast[len(broadcast) - 1] -1)

    return (first_host, last_host)

# Find number of possible hosts
def ip_hosts(ip: str, mask: str) -> list:
    if cidr_32(mask):
        return [1, 0]

    mask_octets = ip_octets_int(mask)
    broadcast = ip_broadcast(ip, mask)
    host_octects = []
    
    for i, mask_octet in enumerate(mask_octets):
        if mask_octet < 255:
            binary_octect = bin(broadcast[i]).replace('0b', '')

            if '0' in binary_octect:
                binary_octect = binary_octect[binary_octect.rindex('0') + 1:]

            host_octects.append(binary_octect)

    host_bits = len(''.join(host_octects))
    hosts = 2**host_bits

    return [hosts, hosts - 2]

'''
Convert this into a cli tool

python subnet.py --vlsm <ip> <subnet_mask>
'''

# Display subnet details
def display_subnet_details(**kwargs) -> None:
    class_addr = kwargs['class_addr']
    net_id = kwargs['net_id']
    broadcast = kwargs['broadcast']
    first_host = kwargs['first_host']
    last_host = kwargs['last_host']
    hosts = kwargs['hosts']

    print()
    print('-'*37)
    print('{:<20}| '.format('class:') + class_addr)
    print('-'*37)
    print('{:<20}| '.format('ip address:') + kwargs['ip'])
    print('-'*37)
    print('{:<20}| '.format('subnet mask:') + kwargs['mask'])
    print('-'*37)
    print('{:<20}| '.format('network address:') + '.'.join([str(octet) for octet in net_id]))
    print('-'*37)
    print('{:<20}| '.format('first host:') + '.'.join([str(octet) for octet in first_host]))
    print('-'*37)
    print('{:<20}| '.format('last host:') + '.'.join([str(octet) for octet in last_host]))
    print('-'*37)
    print('{:<20}| '.format('broadcast address:') + '.'.join([str(octet) for octet in broadcast]))       
    print('-'*37)
    print('{:<20}| '.format('number of hosts:') + str(hosts[0]))
    print('-'*37)  
    print('{:<20}| '.format('usable hosts:') + str(hosts[1]))
    print('-'*37)

class SubnetMaskException(Exception):
    def __init__(self, mask):
        self.mask = mask
        self.message = f"Invalid IPv4 subnet mask: {self.mask}"

class IPv4Exception(Exception):
    def __init__(self, ip):
        self.ip = ip
        self.message = f"Invalid IPv4 address: {self.ip}"

# Validate subnet mask
def validate_subnet_mask(mask: str) -> bool:

    if not re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", mask):
        return False

    mask_octets = [int(octet) for octet in mask.split('.')]

    if len(set(mask_octets)) == 1 and list(set(mask_octets))[0] == 0:
        return False

    significant_octet_index = -1
    for index, octect in enumerate(mask_octets):

        if index != len(mask_octets) - 1:
            if octect == 255 and mask_octets[index + 1] not in [128, 192, 224, 240, 248, 252, 254, 255]:
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
        return False

    if significant_octet_index > -1:
        if mask_octets[significant_octet_index] not in [128, 192, 224, 240, 248, 252, 254, 255]:
            return False
        else: return True

# Validate IPv4 addres
def validate_ip(ip: str) -> bool:
    if not re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip):
        return False
    else:
        return True
    
def main():
    parser = ArgumentParser(
        prog='subnet.py',
        description='subnet.py is a subnet calculator. Example.) --ip 192.168.1.1 --mask 255.255.255.0',
        epilog='Please make sure to use the --ip and --mask flags.'
    )

    parser.add_argument('--ip', dest='ip', help='IPv4 address')
    parser.add_argument('--mask', dest='mask', help='IPv4 subnet mask')

    args = parser.parse_args()

    if args.ip == None or args.mask == None:
        parser.print_help()
        exit()

    try:
        if not validate_ip(args.ip):
            raise IPv4Exception(args.ip)
    except IPv4Exception as ip_e:
        print(ip_e.message)
        exit()
        
    try:
        if not validate_subnet_mask(args.mask):
            raise SubnetMaskException(args.mask)
    except SubnetMaskException as mask_e:
        print(mask_e.message)
        exit()
    
    class_addr = ip_class(args.ip)
    net_id = ip_net_id(args.ip, args.mask)
    broadcast = ip_broadcast(args.ip, args.mask)
    first_host, last_host = ip_first_last_host(args.ip, net_id, broadcast)
    hosts = ip_hosts(args.ip, args.mask)

    display_subnet_details(
        class_addr= class_addr,
        ip= args.ip,
        mask= args.mask,
        net_id= net_id,
        broadcast= broadcast,
        first_host= first_host,
        last_host= last_host,
        hosts= hosts
    )

if __name__ == "__main__":
    main()
    
    