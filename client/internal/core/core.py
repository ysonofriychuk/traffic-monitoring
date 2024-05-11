from scapy.interfaces import NetworkInterface
import scapy.all as scapy

from . import config


def get_iface(iface_name=config.IFACE_NAME) -> NetworkInterface:
    d = {
        name: iface_obj for name, iface_obj in scapy.conf.ifaces.items()
    }

    if not config.IFACE_NAME:
        for name, iface_obj in d.items():
            print(f"Name: {name}\n\tObj: {iface_obj}")

        while True:
            iface_name = input("Введите название интерфейса >>> ").lower()
            if iface_name in d:
                break
            print("Неверное название")

    if iface_name not in d:
        raise f"{iface_name} iface not found"

    return d[iface_name.lower()]
