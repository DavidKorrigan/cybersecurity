# Original version
The original version of the Network scanner & sniffer scripts can be found in the 
[Black Hat Python](https://amzn.eu/d/dQtharE) book from Tim Arnold & Justin Seitz.

# Usage
## Network Scanner using UDP
Example:

`python main.py -o network_scanning -t 192.168.178.0/24 -ip 192.168.178.44`

## Network Sniffing
Example:

`python main.py -o network_scanning -ip 192.168.178.44`

## Syn Port scanner
Examples:

`python main.py -o port_scanning -t 192.168.178.44 -r 1-1024`

`python main.py -o port_scanning -t 192.168.178.44 -l 21,22,80,8080`