#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import logging
import signal
import sys
import time
from datetime import datetime

from internal.core import core, config
from internal.server.checker import Checker
from internal.db.db import Database
from internal.server.receiver import Receiver
from internal.server.pinger import Pinger

IFACE = core.get_iface()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"logs/server-{IFACE.ip.replace('.', '_')}.log",
    filemode="a"
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    db_name_moth = datetime.now().strftime("%Y%m")

    db = Database(f"db/{db_name_moth}.sqlite3")
    db.create_tables()

    logger.debug(f"start server [IP = {IFACE.ip}]")

    logger.info(f"IP_SERVER = {config.IP_SERVER}")
    logger.info(f"IPS_MASK = {config.IPS_MASK}")
    logger.info(f"PORT = {config.PORT}")
    logger.info(f"IFACE_NAME = {config.IFACE_NAME}")

    pinger = Pinger(IFACE, db, delay=60*15)
    pinger.start()

    checker = Checker(IFACE, db, delay=60)
    checker.start()

    receiver = Receiver(IFACE, db)
    receiver.start()

    def sigterm_handler(_, __):
        db.hide_all_clients()
        pinger.stop()
        checker.stop()
        receiver.stop()

        time.sleep(5)
        logger.debug("shutdown")
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    while True: pass

