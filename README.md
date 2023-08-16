# subnetting
A cli subnet calculator 🧮 to satisfy your subnetting needs. Have you ever wanted to subnet a network? Well look no further. This is the World Famous 🌎 cli subnet calculator!

## How to use the script

### CLI subnet calculator
```
python subnet.py --net_class B --ip 72.20.2.79 --cidr /19
```
or
```
python subnet.py --net_class B --ip 72.20.2.79 --mask 255.255.224.0
```
### output
```
-------------------------------------
class_addr          | B
-------------------------------------
ip                  | 72.20.2.79
-------------------------------------
mask                | 255.255.224.0
-------------------------------------
cidr                | /19
-------------------------------------
net_addr            | 72.20.0.0
-------------------------------------
broadcast           | 72.20.31.255
-------------------------------------
first_host          | 72.20.0.1
-------------------------------------
last_host           | 72.20.31.254
-------------------------------------
hosts               | 8192
-------------------------------------
usable_hosts        | 8190
-------------------------------------
possible_networks   | 8
-------------------------------------
```

### Output in JSON
```
python subnet.py --net_class B --ip 72.20.2.79 --cidr /19 --json=True
```
or
```
python subnet.py --net_class B --ip 72.20.2.79 --mask 255.255.224.0 --json=True
```
### output
```
[
  {
    "class_addr": "B",
    "ip": "72.20.2.79",
    "mask": "255.255.224.0",
    "cidr": "/19",
    "net_addr": "72.20.0.0",
    "broadcast": "72.20.31.255",
    "first_host": "72.20.0.1",
    "last_host": "72.20.31.254",
    "hosts": 8192,
    "usable_hosts": 8190,
    "possible_networks": 8
  }
]
```
