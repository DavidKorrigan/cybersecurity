from ctypes import *

import socket
import struct

class IP(Structure):
    '''
    Class that can read a packet and parse the header in fields.
    Binary is get into data structure using ctype module.
    '''
    # Structure which set each part of the IP (Internet Protocol header)
    _fields_ = [
        ("version", c_ubyte, 4),    # 4 bit unsigned char
        ("ihl", c_ubyte, 4),
        ("tos", c_ubyte, 8),        # 1 byte unsigned char
        ("len", c_ushort, 16),      # 2 byte unsigned short
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("protocol_num", c_ubyte, 8),
        ("sum", c_ushort, 16),
        ("src", c_uint32, 32),      # 4 byte unsigned int
        ("dst", c_uint32, 32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # Human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
