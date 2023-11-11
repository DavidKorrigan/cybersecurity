import argparse
import threading
import time

from scanner import NetworkScanner
from sniffer import NetworkSniffer

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-o", "--operation", choices=["network_scanning", "port_scanning", "network_sniffing"],
                           required=True, help="IP of the scanner host.")
    argParser.add_argument("-t", "--target", required=False, help="Network or host targeted.")
    argParser.add_argument("-ip", "--local_ip", required=True, help="IP of the scanner/sniffer host.")

    argParser.add_argument("-p", "--protocol", choices=["tcp", "udp"], required=False, help="Network protocol: tcp or udp")

    args = argParser.parse_args()

    if args.operation == "network_scanning":
        scanner = NetworkScanner(args.local_ip, args.target)
        time.sleep(5)

        t = threading.Thread(target=scanner.udp_sender())
        t.start()
        scanner.scan()

    elif args.operation == "port_scanning":
        print("x")

    elif args.operation == "network_sniffing":
        sniffer = NetworkSniffer(args.local_ip)
        sniffer.sniff()
