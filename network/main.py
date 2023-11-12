import argparse
import sys
import threading
import time

from network_scanner import NetworkScanner
from port_scanner import PortScanner
from sniffer import NetworkSniffer

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-o", "--operation", choices=["network_scanning", "port_scanning", "network_sniffing"],
                           required=True, help="IP of the scanner host.")
    argParser.add_argument("-t", "--target", required=False, default=None, help="Network or host targeted.")
    argParser.add_argument("-ip", "--local_ip", required=False, default=None, help="IP of the scanner/sniffer host.")

    argParser.add_argument("-p", "--protocol", choices=["tcp", "udp"], required=False, default=None, help="Network protocol: tcp or udp")
    argParser.add_argument("-r", "--range", required=False, default=None, help="Range of ports to scan")
    argParser.add_argument("-l", "--list", required=False, default=None, help="List of ports to scan")

    args = argParser.parse_args()

    if args.operation == "network_scanning":
        if args.local_ip is not None and args.target is not None:
            scanner = NetworkScanner(args.local_ip, args.target)
            time.sleep(5)

            t = threading.Thread(target=scanner.udp_sender())
            t.start()
            scanner.scan()
        else:
            print("Local IP & target must be provided.")

    elif args.operation == "port_scanning":
        if args.target is not None:
            if args.range is not None or args.list is not None:
                scanner = PortScanner(args.target, args.range)
                scanner.syn_scan()
            else:
                print("Range or list of ports must be provided.")
                sys.exit(1)
        else:
            print("Target must be provided.")

    elif args.operation == "network_sniffing":
        if args.local_ip is not None:
            sniffer = NetworkSniffer(args.local_ip)
            sniffer.sniff()
        else:
            print("Local IP must be provided.")
