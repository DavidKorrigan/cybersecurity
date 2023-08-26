import socket
import os
import sys

import IP_decoder_ctypes
import IP_decoder_struct

# Possible values: ctypes or struct
IP_DECODER = "struct"

def main(host):
    # Create raw socket, bind to public interface
    if os.name == 'nt':
        # MS Windows let to sniff all incoming packets regardless of protocols
        socket_protocol = socket.IPPROTO_IP
    else:
        # Linux forces to specify which packets to sniff (ICMP here)
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    # Include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Turn on promiscuous mode for MS Windows machine
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # Read a packet
            raw_buffer = sniffer.recvfrom(65565)[0]

            ip_header = None

            if IP_DECODER == "ctypes":
                # Decode using IP class from IP_decoder_ctypes
                ip_header = IP_decoder_ctypes.IP(raw_buffer)
            elif IP_DECODER == "struct":
                # Decode IP header using IP class from IP_decoder_struct sending the 20 first bytes
                ip_header = IP_decoder_struct.IP(raw_buffer[0:20])

            if ip_header.protocol == "ICMP":
                # Print ICMP decoding.
                print(f'Protocol {ip_header.protocol} version {ip_header.ver} - '
                      f'Header length: {ip_header.ihl} Time To Live: {ip_header.ttl} - '
                      f'{ip_header.src_address} -> {ip_header.dst_address}')
            else:
                # Print the detected protocol and hosts.
                print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))



    except KeyboardInterrupt:
        # Turn off promiscuous mode for MS Windows machine
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # Host to listen on
        host = sys.argv[1]
    else:
        # Host to listen on
        host = '192.168.178.31'
    main(host)
