import random

from .settings import SETTINGS


class Client:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac
        self.variant = random.choice(list(SETTINGS.keys()))
