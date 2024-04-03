import time
from threading import Thread, Lock

import scapy.all as scapy
from scapy.interfaces import NetworkInterface

from ..core import core, settings
from ..core.builder import PacBuilder
from ..db.db import Database


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

            clients = core.get_clients()

            self.db.add_clients_if_not_exist(
                [(c.ip, c.mac) for c in clients]
            )

            self.db.add_logs_last_time_in_network(
                [c.ip for c in clients]
            )

            for client in clients:
                print(f"{self.iface.ip} >>> {client.ip} | REQUEST 'check->{client.variant}'")

                pac_builder: PacBuilder = settings.SETTINGS[client.variant]
                scapy.send(
                    pac_builder.build_pac(client.ip, f"check->{client.variant}"),
                    iface=self.iface,
                    verbose=0
                )

            if self.delay:
                time.sleep(self.delay)

    def stop(self):
        self.mutex.acquire()
        self.is_run = False
        self.mutex.release()
