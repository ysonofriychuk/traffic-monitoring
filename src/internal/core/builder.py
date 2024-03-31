import scapy.all as scapy
from scapy.layers.inet import IP, TCP

from . import config


class PacBuilder:
    def __init__(self, tos, ip_flags, ttl, urgptr, tcp_flags, seq, ack):
        self.tos = tos
        self.ip_flags = ip_flags
        self.ttl = ttl
        self.urgptr = urgptr
        self.tcp_flags = tcp_flags
        self.seq = seq
        self.ack = ack

    def ip_settings(self):
        return {
            'tos': self.tos, 'flags': self.ip_flags, 'ttl': self.ttl
        }

    def tcp_settings(self):
        return {
            'urgptr': self.urgptr, 'flags': self.tcp_flags, 'seq': self.seq, 'ack': self.ack
        }

    def build_pac(self, dst_ip: str, message: str, sport=int(config.PORT), dport=int(config.PORT)):
        ip_pac = IP(dst=dst_ip, **self.ip_settings())
        tcp_pac = TCP(sport=sport, dport=dport, **self.tcp_settings())
        raw_pac = scapy.Raw(load=message)

        return ip_pac / tcp_pac / raw_pac

