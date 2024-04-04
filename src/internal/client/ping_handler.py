import scapy.all as scapy
from scapy.fields import FlagValue
from scapy.layers.inet import IP, TCP
from scapy.interfaces import NetworkInterface

from ..core import config
from ..core.settings import SETTINGS


def handler(raw_pac: scapy.Raw):
    raw_load: bytes = raw_pac.load
    raw_load_str: str = raw_load.decode("utf-8")

    return raw_load_str.replace("ping->", "")
