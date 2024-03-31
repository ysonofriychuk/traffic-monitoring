#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import datetime

from internal.core import core
from internal.core import settings
from internal.server import check_send


if __name__ == '__main__':
    iface = core.get_iface()

    print("Сервер запущен")
    while True:
        for client in core.get_clients():
            print(f"\t[{datetime.datetime.now()}] Send request 'var={client.variant}' >>> {client.ip}")
            check_send.send(iface, client, settings.SETTINGS[client.variant])
