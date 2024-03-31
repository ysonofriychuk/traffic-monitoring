#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import scapy.all as scapy
from scapy.layers.inet import IP, TCP

from internal.core import core
from internal.core import config

from internal.client import ping_handler
from internal.client import check_handler

IFACE = core.get_iface()


def proc_func(packet: scapy.packet.Packet):
    ip_pac: IP = packet.getlayer(IP)
    tcp_pac: TCP = packet.getlayer(TCP)
    raw_pac: scapy.Raw = packet.getlayer(scapy.Raw)

    # Пропуск всех невалидных пакетов
    if any([not ip_pac, not tcp_pac, not raw_pac, ip_pac.src != config.IP_SERVER]):
        return

    raw_load: bytes = raw_pac.load
    cmd = raw_load.decode("utf-8")

    print(f"Request '{cmd}' <<<", ip_pac.src)

    if cmd == "ping":
        ping_handler.handler(IFACE, ip_pac, tcp_pac, raw_pac)
    elif cmd.startswith("check->"):
        check_handler.handler(IFACE, ip_pac, tcp_pac, raw_pac)
    else:
        print(f"\tUnknown cmd")


if __name__ == "__main__":
    print("Клиент запущен")
    scapy.sniff(filter=config.FILTER_PAC, prn=proc_func, iface=IFACE)
