from scapy.interfaces import NetworkInterface
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

from . import config
from . import client


def get_iface(iface_name=config.IFACE_NAME) -> NetworkInterface:
    for name, iface_obj in scapy.conf.ifaces.items():
        if name.lower() == iface_name.lower():
            return iface_obj

    raise f"{iface_name} iface not found"


def get_clients() -> list[client.Client]:
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=config.IPS_MASK)

    answers, unanswered = srp(ether / arp, timeout=1, iface=get_iface(), inter=0.1, verbose=False)

    clients = []
    for _, received in answers:
        clients.append(
            client.Client(ip=received.psrc, mac=received.hwsrc)
        )

    return clients
