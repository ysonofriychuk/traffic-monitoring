#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import signal
import sys
from datetime import datetime

from internal.core import core
from internal.server.checker import Checker
from internal.db.db import Database
from internal.server.receiver import Receiver

if __name__ == '__main__':
    iface = core.get_iface()

    db_name_moth = datetime.now().strftime("%Y%m")

    db = Database(f"db/{db_name_moth}.sqlite3")
    db.create_tables()

    print(f"Сервер запущен [IP = {iface.ip}]")

    checker = Checker(iface, db)
    checker.start()

    receiver = Receiver(iface, db)
    receiver.start()

    def sigterm_handler(_, __):
        print("Завершение работы...")
        checker.stop()
        receiver.stop()

        checker.join()
        receiver.join()
        print("Сервер остановлен")
        sys.exit(0)


    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    while True: pass

