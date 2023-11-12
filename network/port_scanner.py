from scapy.layers.inet import IP, TCP, ICMP
from scapy.sendrecv import sr1
from scapy.volatile import RandShort


class PortScanner:
    def __init__(self, target, ip_range=None, ip_list=None, display_closed_ports=False):

        self.target = target
        self.display_closed_ports = display_closed_ports

        if ip_range is not None:
            port_range = ip_range.split("-")
            self.ports = range(int(port_range[0]), int(port_range[1]))
        if ip_list is not None:
            self.ports = ip_list.split(",")
            for i in range(0, len(self.ports)):
                self.ports[i] = int(self.ports[i])

    def syn_scan(self):
        try:
            print(f'SYN scan on {self.target} with ports {self.ports}')
            sport = RandShort()

            open_ports = []

            for port in self.ports:
                packet = sr1(IP(dst=self.target)/TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
                if packet is not None:
                    if packet.haslayer(TCP):
                        # 16 (ACK) + 4 (RST)
                        if packet[TCP].flags == 20:
                            if self.display_closed_ports is True:
                                print(f'Port {port} Closed')
                        # 16 (ACK) + 2 (SYN)
                        elif packet[TCP].flags == 18:
                            print(f'Port {port} Opened')
                            open_ports.append(port)
                        else:
                            print(f'TCP packet response is filtered on port {port}')
                    elif packet.haslayer(ICMP):
                        print(f'ICMP response is filtered on port {port}')
                    else:
                        print(f'Unknown response on port {port}')
                        print(packet.summary())
                else:
                    print(f'No answer on port {port}')
            return open_ports
        except Exception as e:
            print(f'An error occurred:\n{e}')
