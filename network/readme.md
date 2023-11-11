# Original version
The original version of the Network scanner & sniffer scripts can be found in the 
[Black Hat Python](https://amzn.eu/d/dQtharE) book from Tim Arnold & Justin Seitz.

# Usage
## Network Scanner using UDP
python main.py -o network_scanning -t 192.168.178.0/24 -ip 192.168.178.44

## Network Sniffing
python main.py -o network_scanning -ip 192.168.178.44

## Port scanner
python main.py -o port_scanning -t 192.168.178.44