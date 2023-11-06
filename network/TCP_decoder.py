import struct

class TCP:
    '''
    Class that can read TCP packets and parse the header in fields.
    Binary is get into data structure using struct module.
    '''
    def __init__(self, socket_buffer=None):
        cflags = {
            32: "U",    # URGENT
            16: "A",    # ACK
            8: "P",     # PUSH
            4: "R",     # RESET
            2: "S",     # SYN
            1: "F"      # FIN
        }

        # Structure which set each part of the TCP header
        header = struct.unpack("!HHLLBBHHH", socket_buffer)

        self.src_port = header[0]
        self.dst_port = header[1]
        self.seq = header[2]
        self.ack = hex(header[3])  # Acknowledgment: This 1-bit field is used during connection establishment (3-way handshaking) and data transfer.
        self.flags = ""
        for f in cflags:
            if header[5] & f:
                self.flags += cflags[f]

        self.window = header[6]  # This parameter represents the buffer capacity at the receiver’s end. The size of the window is used to manage the flow of data.
        self.checksum = hex(header[7])
        self.urg = header[8]  # Urgent pointer: The urgent pointer points to the end of urgent data in the segment. However, this field appears only if the URG flag is set.