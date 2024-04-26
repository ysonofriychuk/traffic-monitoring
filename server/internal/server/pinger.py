import logging
import time
from threading import Thread, Lock

import scapy.all as scapy
from scapy.interfaces import NetworkInterface
from scapy.layers.inet import IP, TCP

from ..core import core, config
from ..db.db import Database


logger = logging.getLogger(__name__)


class Pinger(Thread):
    def __init__(self, iface: NetworkInterface, db: Database, delay=None):
        super().__init__(daemon=True)

        self.iface: NetworkInterface = iface
        self.db: Database = db

        self.delay = delay

        self.mutex = Lock()
        self.is_run = True

    def run(self):
        copy_is_run = self.is_run
        while copy_is_run:
            self.mutex.acquire()
            copy_is_run = self.is_run
            self.mutex.release()

            clients = core.get_clients(self.iface)

            self.db.update_clients_info(
                [(c.ip, c.mac, c.variant) for c in clients]
            )

            for client in clients:
                ip_pac = IP(dst=client.ip)
                tcp_pac = TCP(sport=int(config.PORT), dport=int(config.PORT))
                raw_pac = scapy.Raw(load=f"ping->{client.variant}")

                pac = ip_pac / tcp_pac / raw_pac

                logger.info(f"outgoing request {self.iface.ip} >>> {client.ip}, raw = ping->{client.variant}")

                scapy.send(pac, iface=self.iface, verbose=0)

            if self.delay:
                time.sleep(self.delay)

    def stop(self):
        self.mutex.acquire()
        self.is_run = False
        self.mutex.release()

