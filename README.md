# subnetting
A cli subnet calculator 🧮 to satisfy your subnetting needs. Have you ever wanted to subnet a network? Well look no further. This is the World Famous 🌎 cli subnet calculator!

## How to use the script

### CLI subnet calculator
```
python subnet.py --net_class A --ip 72.20.2.79 --mask 255.255.255.0
```
### output
```
-------------------------------------
class_addr          | A
-------------------------------------
ip                  | 72.20.2.79
-------------------------------------
mask                | 255.255.255.0
-------------------------------------
net_addr            | 72.20.2.0
-------------------------------------
broadcast           | 72.20.2.255
-------------------------------------
first_host          | 72.20.2.1
-------------------------------------
last_host           | 72.20.2.254
-------------------------------------
hosts               | 256
-------------------------------------
usable_hosts        | 254
-------------------------------------
possible_networks   | 65536
-------------------------------------
```

### Output in JSON
```
python subnet.py --net_class C --ip 72.20.2.79 --mask 255.255.255.128 --json=true
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
