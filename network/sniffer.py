import socket
import os
import sys

import IP_decoder_ctypes
import IP_decoder_struct
from ICMP_decoder import ICMP
from TCP_decoder import TCP


# Possible values: ctypes or struct
IP_DECODER = "struct"


class NetworkSniffer:
    def __init__(self, host):
        self.host = host

        # Create raw socket, bind to public interface
        if os.name == 'nt':
            # MS Windows let to sniff all incoming packets regardless of protocols
            socket_protocol = socket.IPPROTO_IP
        else:
            # Linux forces to specify which packets to sniff (ICMP here)
            socket_protocol = socket.IPPROTO_ICMP

        try:
            self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
            self.sniffer.bind((host, 0))
            # Include the IP header in the capture
            self.sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            # Turn on promiscuous mode for MS Windows machine
            if os.name == 'nt':
                self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except Exception as e:
            print(f'An error occurred:\n{e}')
            sys.exit(1)

    def sniff(self):
        try:
            while True:
                # Read a packet
                raw_buffer = self.sniffer.recvfrom(65565)[0]

                ip_header = None

                if IP_DECODER == "ctypes":
                    # Decode using IP class from IP_decoder_ctypes
                    ip_header = IP_decoder_ctypes.IP(raw_buffer)
                elif IP_DECODER == "struct":
                    # Decode IP header using IP class from IP_decoder_struct sending the 20 first bytes
                    ip_header = IP_decoder_struct.IP(raw_buffer[0:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    icmp_header = ICMP(raw_buffer[offset:offset + 8])
                    # Identify default ICMP code
                    if icmp_header.type == 3 or icmp_header.type == 5 or icmp_header.type == 11 or icmp_header.type == 12:
                        icmp_code_name = " & Code: " + icmp_header.code_name
                    else:
                        icmp_code_name = ""
                    # Print ICMP decoding
                    print(f'IPv{ip_header.ver} - Protocol {ip_header.protocol} - '
                          f'Type: {icmp_header.type_name}{icmp_code_name} - '
                          f'Header length: {ip_header.ihl} Time To Live: {ip_header.ttl} - '
                          f'{ip_header.src_address} -> {ip_header.dst_address}')
                elif ip_header.protocol == "TCP":
                    tcp_header = TCP(raw_buffer[0:20])
                    print(f'IPv{ip_header.ver} - Protocol {ip_header.protocol} - '
                          f'{ip_header.src_address}:{tcp_header.src_port} -> {ip_header.dst_address}:{tcp_header.dst_port} - '
                          f'Flags set: {tcp_header.flags}')
                else:
                    # Print the detected protocol and hosts.
                    print(f'IPv{ip_header.ver} - Protocol {ip_header.protocol} - '
                          f'{ip_header.src_address} -> {ip_header.dst_address}')
        except KeyboardInterrupt:
            # Turn off promiscuous mode for MS Windows machine
            if os.name == 'nt':
                self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            sys.exit()
