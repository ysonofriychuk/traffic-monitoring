import logging
import time
from threading import Thread, Lock

import scapy.all as scapy
from scapy.interfaces import NetworkInterface

from ..core import settings
from ..core.builder import PacBuilder
from ..db.db import Database


logger = logging.getLogger(__name__)


class Checker(Thread):
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

            clients_info = self.db.get_clients_info()

            for client_info in clients_info:
                ip, variant = client_info

                logger.info(f"outgoing request {self.iface.ip} >>> {ip}, raw = check->{variant}")

                pac_builder: PacBuilder = settings.SETTINGS[variant]
                scapy.send(
                    pac_builder.build_pac(ip, f"check->{variant}"),
                    iface=self.iface,
                    verbose=0
                )

            if self.delay:
                time.sleep(self.delay)

    def stop(self):
        self.mutex.acquire()
        self.is_run = False
        self.mutex.release()
