# Written by eriaht 08/12/23

import re
import json
from argparse import ArgumentParser

network_classes = {
    "A": {
        "bits": 8,
    },
    "B": {
        "bits": 16
    },
    "C": {
        "bits": 24
    }
}

# Create a list of containing each octet as an int
def ip_octets_int(ip: str) -> list:
    return [int(octet) for octet in ip.split(".")]

# Convert IP to binary
def ip_to_bin(ip: str) -> list:
    octets_dec = ip_octets_int(ip)
    octets_bin = [f"{bin(octect).replace('0b', ''):>08}" for octect in octets_dec]
    
    return octets_bin

# Find network address
def ip_net_addr(ip: str, mask: str) -> list:
    ip_octets = ip_octets_int(ip)
    mask_octets = ip_octets_int(mask)
    net_addr = []

    for i in range(len(ip_octets)):
        net_addr.append(ip_octets[i] & mask_octets[i])

    return net_addr

def cidr_32(mask: str) -> bool:
    mask_octets = [int(octet) for octet in mask.split(".")]

    if len(set(mask_octets)) == 1 and list(set(mask_octets))[0] == 255:
        return True
    
    return False

# Find the significant octet index
def find_significant_octet(mask: str) -> int:
    mask_octets = [int(octet) for octet in mask.split(".")]

    significant_octet_index = -1
    for index, octect in enumerate(mask_octets):

        if index != len(mask_octets) - 1:
            if octect == 255 and mask_octets[index + 1] not in [128, 192, 224, 240, 248, 252, 254, 255]:
                significant_octet_index = index
                break

        if octect in range(1, 255):
            significant_octet_index = index
            break

    return significant_octet_index

# Find number of subnets
def calc_subnets(mask: str, net_class: str) -> int:
    mask_bits = len(("".join(ip_to_bin(mask))).replace("0", ""))

    return 2**abs(mask_bits - network_classes[net_class]["bits"])
    

# Find broadcast address
def ip_broadcast(ip: str, mask: str) -> list:
    if cidr_32(mask):
        return ip_octets_int(ip)

    net_addr = ip_net_addr(ip, mask)
    mask_octets = ip_octets_int(mask)
    broadcast_addr = []

    for i, mask_octet in enumerate(mask_octets):
        if mask_octet == 255:
            broadcast_addr.append(net_addr[i])
        elif mask_octet < 255:
            if net_addr[i] > 0:
                """
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
                """
                broadcast_addr.append(((net_addr[i] | mask_octets[i]) ^ 255) + net_addr[i])
            else:
                broadcast_addr.append((net_addr[i] | mask_octets[i]) ^ 255)

    return broadcast_addr

# Find first and last host addresses
def ip_first_last_host(ip:str, net_addr: list, broadcast: list) -> tuple:
    first_host = None
    last_host = None
    if ip_octets_int(ip) == broadcast:
        return (ip_octets_int(ip), "")

    first_host = net_addr[0:len(net_addr) - 1]
    first_host.append(net_addr[len(net_addr) - 1] + 1)

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
            binary_octect = bin(broadcast[i]).replace("0b", "")

            if "0" in binary_octect:
                binary_octect = binary_octect[binary_octect.rindex("0") + 1:]

            host_octects.append(binary_octect)

    host_bits = len("".join(host_octects))
    hosts = 2**host_bits

    return [hosts, hosts - 2]

# Display subnet details
def display_subnet_details(**kwargs) -> None:
    subnet_details = {
        "class_addr": kwargs["class_addr"],
        "ip": kwargs["ip"],
        "mask": kwargs["mask"],
        "net_addr":".".join([str(octet) for octet in kwargs["net_addr"]]),
        "broadcast": ".".join([str(octet) for octet in kwargs["broadcast"]]),
        "first_host": ".".join([str(octet) for octet in kwargs["first_host"]]),
        "last_host": ".".join([str(octet) for octet in kwargs["last_host"]]),
        "hosts": kwargs["hosts"][0],
        "usable_hosts": kwargs["hosts"][1],
        "possible_networks": kwargs["networks"]
    }

    if kwargs["json"]:
        print(json.dumps([subnet_details], indent=2))
    else:
        print()
        print("-"*37)
        for key, value in subnet_details.items():
            if type(value) is int:
                value = str(value)
            print("{:<20}| ".format(key) + value)
            print("-"*37)

class SubnetMaskException(Exception):
    def __init__(self, mask):
        self.mask = mask
        self.message = f"Invalid IPv4 subnet mask: {self.mask}"

class IPv4Exception(Exception):
    def __init__(self, ip):
        self.ip = ip
        self.message = f"Invalid IPv4 address: {self.ip}"

class NetworkClassException(Exception):
    def __init__(self, mask, net_class):
        self.net_class = net_class
        self.mask = mask
        self.message = f"The subnet mask {self.mask} is smaller than the default mask for network class {self.net_class}"

# validate network with mask
def validate_network(mask: str, net_class: str) -> bool:
    mask_bits = len(("".join(ip_to_bin(mask))).replace("0", ""))

    if mask_bits - network_classes[net_class]["bits"] < 0:
        return False
    
    return True

# Validate subnet mask
def validate_subnet_mask(mask: str) -> bool:

    if not re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", mask):
        return False

    mask_octets = [int(octet) for octet in mask.split(".")]

    if len(set(mask_octets)) == 1 and list(set(mask_octets))[0] == 0:
        return False

    significant_octet_index = find_significant_octet(mask)

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
        prog="subnet.py",
        description="subnet.py is a subnet calculator. Example.) --net_class C --ip 192.168.1.1 --mask 255.255.255.0",
        epilog="Please make sure to use the --ip and --mask flags."
    )

    parser.add_argument("--net_class", dest="net_class", help="IPv4 network class")
    parser.add_argument("--ip", dest="ip", help="IPv4 address")
    parser.add_argument("--mask", dest="mask", help="IPv4 subnet mask")
    parser.add_argument("--json", dest="json", default=False, help="Add this argument if you want the details in json. The default value is False.")

    args = parser.parse_args()

    if (
        args.ip == None or 
        args.mask == None or 
        args.net_class == None
    ):
        parser.print_help()
        exit()

    try:
        if not validate_network(args.mask, args.net_class):
            raise NetworkClassException(args.mask, args.net_class)
    except NetworkClassException as class_e:
        print(class_e.message)
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
    
    class_addr = args.net_class
    net_addr = ip_net_addr(args.ip, args.mask)
    broadcast = ip_broadcast(args.ip, args.mask)
    first_host, last_host = ip_first_last_host(args.ip, net_addr, broadcast)
    hosts = ip_hosts(args.ip, args.mask)
    networks = calc_subnets(args.mask, args.net_class)

    display_subnet_details(
        json= args.json,
        class_addr= class_addr,
        ip= args.ip,
        mask= args.mask,
        net_addr= net_addr,
        broadcast= broadcast,
        first_host= first_host,
        last_host= last_host,
        hosts= hosts,
        networks= networks
    )

if __name__ == "__main__":
    main()
    
    