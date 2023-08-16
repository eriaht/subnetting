# subnetting
A cli subnet calculator.
```
python subnet.py -h
usage: subnet.py [-h] [--net_class NET_CLASS] [--ip IP] [--mask MASK]

subnet.py is a subnet calculator. Example.) --net_class C --ip 192.168.1.1 --mask 255.255.255.0

options:
  -h, --help            show this help message and exit
  --net_class NET_CLASS
                        IPv4 network class
  --ip IP               IPv4 address
  --mask MASK           IPv4 subnet mask

Please make sure to use the --ip and --mask flags.
```

## How to use the script

### CLI subnet calculator
```
python subnet.py --ip 72.20.2.79 --mask 255.255.224.0
```
### output
```
-------------------------------------
class:              | A
-------------------------------------
ip address:         | 72.20.2.79
-------------------------------------
subnet mask:        | 255.255.224.0
-------------------------------------
network address:    | 72.20.0.0
-------------------------------------
first host:         | 72.20.0.1
-------------------------------------
last host:          | 72.20.31.254
-------------------------------------
broadcast address:  | 72.20.31.255
-------------------------------------
number of hosts:    | 8192
-------------------------------------
usable hosts:       | 8190
-------------------------------------
```

### Output in JSON
```
python subnet.py --ip 72.20.2.79 --mask 255.255.224.0 --json=true
```
### output
```
[
  {
    "class_addr": "C",
    "ip": "72.20.2.79",
    "mask": "255.255.255.128",
    "net_addr": "72.20.2.0",
    "broadcast": "72.20.2.127",
    "first_host": "72.20.2.1",
    "last_host": "72.20.2.126",
    "hosts": 128,
    "usable_hosts": 126,
    "possible_networks": 2
  }
]
```
