import logging

import scapy.all as scapy
from scapy.fields import FlagValue
from scapy.layers.inet import IP, TCP
from scapy.interfaces import NetworkInterface

from ..core import config
from ..core.settings import SETTINGS


logger = logging.getLogger(__name__)


def reliability_coefficient(ip_pac: IP, tcp_pac: TCP, raw_pac: scapy.Raw, variant: str) -> float:
    """
    Функция вычисления коэффициента достоверности

    :param ip_pac: IP слой
    :param tcp_pac: TCP слой
    :param raw_pac: RAW
    :param variant: вариант настроек
    :return: Значение в диапазоне от 0.0 до 1.0
    """
    if any([not tcp_pac, not ip_pac, not raw_pac]):
        return 0

    settings = SETTINGS.get(variant)
    if not settings:
        return 0

    raw_load: bytes = raw_pac.load
    raw_load_str: str = raw_load.decode("utf-8")
    msg = raw_load_str.replace("check->", "")

    tcp_flags: FlagValue = tcp_pac.flags
    ip_flags: FlagValue = ip_pac.flags

    ip_tos: int = ip_pac.tos
    ip_flags_value: int = ip_flags.value
    ip_ttl: int = ip_pac.ttl

    expected_ip_tos: int = settings.tos
    expected_ip_flags_value: int = settings.ip_flags
    expected_ip_ttl: int = settings.ttl

    tcp_urgptr: int = tcp_pac.urgptr
    tcp_flags_value: int = tcp_flags.value
    tcp_seq: int = tcp_pac.seq
    tcp_ack: int = tcp_pac.ack

    expected_tcp_urgptr: int = settings.urgptr
    expected_tcp_flags_value: int = settings.tcp_flags
    expected_tcp_seq: int = settings.seq
    expected_tcp_ack: int = settings.ack

    checks = [
        ip_tos == expected_ip_tos,
        ip_flags_value == expected_ip_flags_value,
        ip_ttl == expected_ip_ttl,
        tcp_urgptr == expected_tcp_urgptr,
        tcp_flags_value == expected_tcp_flags_value,
        tcp_seq == expected_tcp_seq,
        tcp_ack == expected_tcp_ack,
        msg == variant,
    ]

    return sum(checks) / len(checks) if checks else 0


def handler(iface: NetworkInterface, ip_pac: IP, tcp_pac: TCP, raw_pac: scapy.Raw, variant: str):
    k = reliability_coefficient(ip_pac, tcp_pac, raw_pac, variant)

    ip_pac = IP(dst=ip_pac.src)
    tcp_pac = TCP(sport=int(config.PORT), dport=int(config.PORT))
    raw_pac = scapy.Raw(load=f"answer->{round(k, 3)}")

    pac = ip_pac / tcp_pac / raw_pac

    logger.info(f"outgoing request {iface.ip} >>> {ip_pac.src}, raw = answer->{round(k, 3)}")
    scapy.send(pac, iface=iface, verbose=0)
