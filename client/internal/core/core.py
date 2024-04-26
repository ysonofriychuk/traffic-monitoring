from scapy.interfaces import NetworkInterface
import scapy.all as scapy

from . import config


def get_iface(iface_name=config.IFACE_NAME) -> NetworkInterface:
    for name, iface_obj in scapy.conf.ifaces.items():
        if name.lower() == iface_name.lower():
            return iface_obj

    raise f"{iface_name} iface not found"
