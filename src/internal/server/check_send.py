import scapy.all as scapy
from scapy.interfaces import NetworkInterface

from ..core.builder import PacBuilder
from ..core.client import Client


def send(iface: NetworkInterface, client: Client, pac_builder: PacBuilder):
    scapy.send(pac_builder.build_pac(client.ip, f"check->{client.variant}"), iface=iface, verbose=0)
