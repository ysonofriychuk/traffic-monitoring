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


