import logging
from threading import Thread

import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.interfaces import NetworkInterface

from ..core import config
from ..db.db import Database


logger = logging.getLogger(__name__)


class Receiver(Thread):
    def __init__(self, iface: NetworkInterface, db: Database):
        super().__init__(daemon=True)

        self.iface: NetworkInterface = iface
        self.db: Database = db

        self.is_run = True

    def run(self):
        scapy.sniff(filter=config.FILTER_PAC_SERVER, prn=self.__handler, iface=self.iface, stop_filter=self.__stop_filter)

    def stop(self):
        self.is_run = False

    def __stop_filter(self, _):
        return not self.is_run

    def __handler(self, packet: scapy.packet.Packet):
        ip_pac: IP = packet.getlayer(IP)
        tcp_pac: TCP = packet.getlayer(TCP)
        raw_pac: scapy.Raw = packet.getlayer(scapy.Raw)

        # Пропуск всех невалидных пакетов
        if any([not ip_pac, not tcp_pac, not raw_pac, ip_pac.src == self.iface.ip]):
            return

        msg = raw_pac.load.decode("utf-8") if raw_pac.load else ""

        logger.info(f"incoming request {ip_pac.src} >>> {self.iface.ip}, raw = {msg}")

        if not msg.startswith("answer->"):
            return

        answer: float
        try:
            answer = float(msg.replace("answer->", ""))
            self.db.add_log_confidence_factor(ip_pac.src, answer)
        except ValueError as e:
            logger.error(f"error parse: {e}")
            return


