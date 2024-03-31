import scapy.all as scapy
from scapy.interfaces import NetworkInterface
from scapy.layers.inet import IP, TCP


def handler(iface: NetworkInterface, ip_pac: IP, tcp_pac: TCP, raw_pac: scapy.Raw):
    pass
