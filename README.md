# subnetting
Two separate scripts. One for classful subnetting, the other for classless or VLSM subnetting.

I am currently studying for the Network+ and I have always wanted my own subnet calculator so here it is.

## How to use the scripts

### Classful subnetting
```
python classful_sub.py
```
### output
```
Enter ip address: 192.168.1.1

           class C address           
-------------------------------------
ip address:         | 192.168.1.1
-------------------------------------
subnet mask:        | 255.255.255.0
-------------------------------------
network address:    | 192.168.1.0
-------------------------------------
first host:         | 192.168.1.1
-------------------------------------
last host:          | 192.168.1.254
-------------------------------------
broadcast address:  | 192.168.1.255
-------------------------------------
number of hosts:    | 256
-------------------------------------
usable hosts:       | 254
-------------------------------------
```

### Classless subnetting aka VLSM
```
python classless_sub.py
```

### output
```
Enter ip address: 172.20.2.79
Enter subnet mask: 255.255.224.0

-------------------------------------
ip address:         | 172.20.2.79
-------------------------------------
network address:    | 172.20.0.0
-------------------------------------
first host:         | 172.20.0.1
-------------------------------------
last host:          | 172.20.31.254
-------------------------------------
broadcast address:  | 172.20.31.255
-------------------------------------
number of hosts:    | 8192
-------------------------------------
usable hosts:       | 8190
-------------------------------------
```
