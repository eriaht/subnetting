def ip_octets_int(ip) -> list:
    return [int(octet) for octet in ip.split('.')]

def ip_octets_str(ip) -> list:
    return ip.split('.')

# Determine the IP address class
def ip_class(ip) -> str:
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
    
# Subnet mask
def ip_subnet_mask(ip_cl) -> str:
    subnet_mask = None
    if ip_cl == 'A':
        subnet_mask = '255.0.0.0'
    elif ip_cl == 'B':
        subnet_mask = '255.255.0.0'
    elif ip_cl == 'C':
        subnet_mask = '255.255.255.0'
    
    return subnet_mask
    
# Network address
def ip_network_address(ip, ip_cl) -> str:
    octets = ip_octets_str(ip)
    network_addr = None
    if ip_cl == 'A':
        network_addr = f'{octets[0]}.0.0.0'
    elif ip_cl == 'B':
        network_addr = f'{octets[0]}.{octets[1]}.0.0'
    elif ip_cl == 'C':
        network_addr = f'{octets[0]}.{octets[1]}.{octets[2]}.0'

    return network_addr

# First and last available host
def ip_first_last_host(ip, ip_cl) -> tuple:
    octets = ip_octets_str(ip)
    first_host = None
    last_host = None
    if ip_cl == 'A':
        first_host = f'{octets[0]}.0.0.1'
        last_host = f'{octets[0]}.255.255.254'
    elif ip_cl == 'B':
        first_host = f'{octets[0]}.{octets[1]}.0.1'
        last_host = f'{octets[0]}.{octets[1]}.255.254'
    elif ip_cl == 'C':
        first_host = f'{octets[0]}.{octets[1]}.{octets[2]}.1'
        last_host = f'{octets[0]}.{octets[1]}.{octets[2]}.254'

    return (first_host, last_host)

# Broadcast address
def ip_broadcast(ip, ip_cl) -> str:
    octets = ip_octets_str(ip)
    broadcast_addr = None
    if ip_cl == 'A':
        broadcast_addr = f'{octets[0]}.255.255.255'
    elif ip_cl == 'B':
        broadcast_addr = f'{octets[0]}.{octets[1]}.255.255'
    elif ip_cl == 'C':
        broadcast_addr = f'{octets[0]}.{octets[1]}.{octets[2]}.255'

    return broadcast_addr

# Last available host
def ip_subnet_details(ip, ip_cl):
    subnet_class = f'class {ip_cl} address'
    subnet_mask = ip_subnet_mask(ip_cl)
    network_address = ip_network_address(ip, ip_cl)
    first_host, last_host = ip_first_last_host(ip, ip_cl)
    broadcast = ip_broadcast(ip, ip_cl)

    print()
    print('{:^37}'.format(subnet_class))
    print('-'*37)
    print('{:<20}| '.format('ip address:') + ip)
    print('-'*37)
    print('{:<20}| '.format('subnet mask:') + subnet_mask)
    print('-'*37)
    print('{:<20}| '.format('network address:') + network_address)
    print('-'*37)
    print('{:<20}| '.format('first host:') + first_host)
    print('-'*37)
    print('{:<20}| '.format('last host:') + last_host)
    print('-'*37)
    print('{:<20}| '.format('broadcast address:') + broadcast)       
    print('-'*37)

if __name__ == '__main__':
    ip = input('Enter ip address for classful subnet details: ')
    ip_subnet_details(ip, ip_class(ip))