# Written by eriaht 08/12/23

from classful_sub import ip_octets_int
from get_valid_ip import get_valid_ip

# Convert IP to binary
def ip_to_bin(ip: str) -> list:
    octets_dec = ip_octets_int(ip)
    octets_bin = [f"{bin(octect).replace('0b', ''):>08}" for octect in octets_dec]
    
    return octets_bin

# Find network address
def ip_net_id(ip: str, mask: str) -> list:
    ip_octets = ip_octets_int(ip)
    mask_octets = ip_octets_int(mask)
    net_id = []

    for i in range(len(ip_octets)):
        net_id.append(ip_octets[i] & mask_octets[i])

    return net_id

# Find broadcast address
def ip_broadcast(ip: str, mask: str) -> list:
    net_id = ip_net_id(ip, mask)
    mask_octets = ip_octets_int(mask)
    broadcast_addr = []

    for i, mask_octet in enumerate(mask_octets):
        if mask_octet == 255:
            broadcast_addr.append(net_id[i])
        elif mask_octet < 255: # <-----------------
            if net_id[i] > 0:
                broadcast_addr.append(((net_id[i] | mask_octets[i]) ^ 255) + net_id[i])
                '''
                Logic for this part
                --------------------
                IP:          137.72.145.170
                Net address: 137.72.144.0
                Subnet Mask: 255.255.248.0

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
            else:
                broadcast_addr.append((net_id[i] | mask_octets[i]) ^ 255)

    return broadcast_addr

# Find first and last host addresses
def ip_first_last_host(net_id: list, broadcast: list) -> tuple:
    first_host = net_id[0:len(net_id) - 1]
    first_host.append(net_id[len(net_id) - 1] + 1)

    last_host = broadcast[0:len(broadcast) - 1]
    last_host.append(broadcast[len(broadcast) - 1] -1)

    return (first_host, last_host)

# Find number of possible hosts
def ip_hosts(ip: str, mask: str) -> int:
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

    return 2**host_bits

# Display subnet details
def ip_subnet_details(ip: str, mask: str) -> None:
    net_id = ip_net_id(ip, mask)
    broadcast = ip_broadcast(ip, mask)
    first_host, last_host = ip_first_last_host(net_id, broadcast)
    hosts = ip_hosts(ip, mask)

    print()
    print('-'*37)
    print('{:<20}| '.format('ip address:') + ip)
    print('-'*37)
    print('{:<20}| '.format('subnet mask:') + subnet_mask)
    print('-'*37)
    print('{:<20}| '.format('network address:') + '.'.join([str(octet) for octet in net_id]))
    print('-'*37)
    print('{:<20}| '.format('first host:') + '.'.join([str(octet) for octet in first_host]))
    print('-'*37)
    print('{:<20}| '.format('last host:') + '.'.join([str(octet) for octet in last_host]))
    print('-'*37)
    print('{:<20}| '.format('broadcast address:') + '.'.join([str(octet) for octet in broadcast]))       
    print('-'*37)
    print('{:<20}| '.format('number of hosts:') + str(hosts))
    print('-'*37)  
    print('{:<20}| '.format('usable hosts:') + str(hosts - 2))
    print('-'*37)   

if __name__ == "__main__":
    ip_address = get_valid_ip()
    subnet_mask = get_valid_ip()

    if ip_address and subnet_mask:
        ip_subnet_details(ip_address, subnet_mask)