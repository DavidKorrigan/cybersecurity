import ipaddress
import socket
import os
import sys
import threading
import time

import IP_decoder_ctypes
import IP_decoder_struct
from ICMP_decoder import ICMP


# Define signature to check responses are from the UDP packets sent
MESSAGE = 'ONLINE'


class NetworkScanner:
    def __init__(self, host, target):
        self.host = host
        self.target = target

        # Create raw socket, bind to public interface
        if os.name == 'nt':
            # MS Windows let to sniff all incoming packets regardless of protocols
            socket_protocol = socket.IPPROTO_IP
        else:
            # Linux forces to specify which packets to sniff (ICMP here)
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        # Include the IP header in the capture
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Turn on promiscuous mode for MS Windows machine
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def scan(self):

        host_up = set([f'{str(self.host)} *'])
        try:
            while True:
                # Read a packet
                raw_buffer = self.socket.recvfrom(65565)[0]
                ip_header = IP_decoder_struct.IP(raw_buffer[0:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    #buf = raw_buffer[offset:offset + sizeof(ICMP)]
                    buf = raw_buffer[offset:offset + 8]

                    # Create our ICMP structure
                    icmp_header = ICMP(buf)

                    # Now check for the TYPE 3 and CODE 3 which indicates
                    # A host is up but no port available to talk to
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        # Check to make sure we are receiving the response that lands in our subnet
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(self.target):
                            # Make sure it has the signature from the message sent.
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                target = str(ip_header.src_address)
                                if target != self.host and target not in host_up:
                                    host_up.add(str(ip_header.src_address))
                                    print("Host Up: %s" % target)

        except KeyboardInterrupt:
            # Turn off promiscuous mode for MS Windows machine
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\nUser interrupted scan.')

            if host_up:
                print(f'\n\nSummary: Hosts up on {self.target}')
                for host in host_up:
                    print(f'{host}')
                print('')
            sys.exit()

    # This function iterates all the IPs from the subnet targeted and sends UDP datagrams
    def udp_sender(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            for ip in ipaddress.ip_network(self.target).hosts():
                sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))
