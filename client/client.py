#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import logging

import scapy.all as scapy
from scapy.layers.inet import IP, TCP

from internal.core import core
from internal.core import config

from internal.client import check_handler, ping_handler

IFACE = core.get_iface()

variant = ""

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"logs/client-{IFACE.ip.replace('.', '_')}.log",
    filemode="a"
)

logger = logging.getLogger(__name__)


def proc_func(packet: scapy.packet.Packet):
    ip_pac: IP = packet.getlayer(IP)
    tcp_pac: TCP = packet.getlayer(TCP)
    raw_pac: scapy.Raw = packet.getlayer(scapy.Raw)

    # Пропуск всех невалидных пакетов
    if any([not ip_pac, not tcp_pac, not raw_pac]):
        # WARNING без print пакеты не обрабатываются ヽ(°□° )ノ
        logger.warning(f"invalid packet: {packet.payload}")
        return

    global variant

    raw_load: bytes = raw_pac.load
    cmd = raw_load.decode("utf-8")

    logger.info(f"incoming request {ip_pac.src} >>> {ip_pac.dst}, raw = {cmd}")

    if cmd.startswith("check->"):
        if not variant:
            logger.warning("variant not set")
            return
        check_handler.handler(IFACE, ip_pac, tcp_pac, raw_pac, variant)

    elif cmd.startswith("ping->"):
        variant = ping_handler.handler(raw_pac)
        logger.debug(f"set variant '{variant}'")


if __name__ == "__main__":
    logger.debug(f"start client [IP = {IFACE.ip}]")

    logger.info(f"IP_SERVER = {config.IP_SERVER}")
    logger.info(f"PORT = {config.PORT}")
    logger.info(f"IFACE_NAME = {config.IFACE_NAME}")

    scapy.sniff(filter=config.FILTER_PAC_CLIENT, prn=proc_func, iface=IFACE)
