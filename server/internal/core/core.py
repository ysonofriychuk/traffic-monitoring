from scapy.interfaces import NetworkInterface
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

from . import config
from . import client


def get_iface(iface_name=config.IFACE_NAME) -> NetworkInterface:
    d = {
        name: iface_obj for name, iface_obj in scapy.conf.ifaces.items()
    }

    if not config.IFACE_NAME:
        for name, _ in d.items():
            print(f"Name: {name}")

        while True:
            iface_name = input("enter interface name: ").lower()
            if iface_name in d:
                break
            print("Wrong name")

    if iface_name not in d:
        raise f"{iface_name} iface not found"

    return d[iface_name.lower()]


def get_clients(iface: NetworkInterface) -> list[client.Client]:
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=config.IPS_MASK)

    answers, unanswered = srp(ether / arp, timeout=1, iface=iface, inter=0.1, verbose=False)

    clients = {}
    for _, received in answers:
        clients[received.psrc] = client.Client(ip=received.psrc, mac=received.hwsrc)

    return list(clients.values())
