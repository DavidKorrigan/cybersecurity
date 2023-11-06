import struct


class ICMP:
    '''
    Class that can read ICMP packets and parse the header in fields.
    Binary is get into data structure using struct module.
    Based on: https://www.ibm.com/docs/en/qsip/7.4?topic=applications-icmp-type-code-ids
    '''
    def __init__(self, buffer):
        header = struct.unpack('<BBHHH', buffer)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

        # Map type constants to their names
        self.icmp_type_map = {
            0: "Echo reply",
            3: "Destination unreachable",
            4: "Source quench",
            5: "Redirect",
            8: "Echo",
            9: "Router advertisement",
            10: "Router selection",
            11: "Time exceeded",
            12: "Parameter problem",
            13: "Timestamp",
            14: "Timestamp reply",
            15: "Information request",
            16: "Information reply",
            17: "Address mask request",
            18: "Address mask reply",
            30: "Traceroute"
        }

        self.type_name = self.icmp_type_map[self.type]


        # Map code constants for type 3 to their names
        self.icmp_code_3_map = {
            0: "Net is unreachable",
            1: "Host is unreachable",
            2: "Protocol is unreachable",
            3: "Port is unreachable",
            4: "Fragmentation is needed and Don't Fragment was set",
            5: "Source route failed",
            6: "Destination network is unknown",
            7: "Destination host is unknown",
            8: "Source host is isolated",
            9: "Communication with destination network is administratively prohibited",
            10: "Communication with destination host is administratively prohibited",
            11: "Destination network is unreachable for type of service",
            12: "Destination host is unreachable for type of service",
            13: "Communication is administratively prohibited",
            14: "Host precedence violation",
            15: "Precedence cutoff is in effect",
        }

        # Map code constants for type 5 to their names
        self.icmp_code_5_map = {
            0: "Redirect datagram for the network (or subnet)",
            1: "Redirect datagram for the host",
            2: "Redirect datagram for the type of service and network",
            3: "Redirect datagram for the type of service and host"
        }

        # Map code constants for type 11 to their names
        self.icmp_code_11_map = {
            0: "Time to Live exceeded in transit",
            1: "Fragment reassembly time exceeded"
        }

        # Map code constants for type 12 to their names
        self.icmp_code_12_map = {
            0: "Pointer indicates the error",
            1: "Missing a required option",
            2: "Bad length"
        }

        if self.type == 3:
            self.code_name = self.icmp_code_3_map[self.code]
        elif self.type == 5:
            self.code_name = self.icmp_code_5_map[self.code]
        elif self.type == 11:
            self.code_name = self.icmp_code_11_map[self.code]
        elif self.type == 12:
            self.code_name = self.icmp_code_12_map[self.code]
