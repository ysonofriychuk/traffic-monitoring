import scapy.all as scapy
from scapy.fields import FlagValue
from scapy.layers.inet import IP, TCP
from scapy.interfaces import NetworkInterface


def reliability_coefficient(ip_pac: IP, tcp_pac: TCP, raw_pac: scapy.Raw) -> float:
    """
    Функция вычисления коэффициента достоверности

    :param ip_pac: IP слой
    :param tcp_pac: TCP слой
    :param raw_pac: RAW
    :return: Значение в диапазоне от 0.0 до 1.0
    """
    if any([not tcp_pac, not ip_pac, not raw_pac]):
        return 0

    tcp_flags: FlagValue = tcp_pac.flags
    ip_flags: FlagValue = ip_pac.flags

    ip_tos: int = ip_pac.tos
    ip_flags_value: int = ip_flags.value if tcp_flags else -1
    ip_ttl: int = ip_pac.ttl

    tcp_urgptr: int = tcp_pac.urgptr
    tcp_flags_value: int = tcp_flags.value if tcp_flags else -1
    tcp_seq: int = tcp_pac.seq
    tcp_ack: int = tcp_pac.ack

    raw_load: bytes = raw_pac.load

    return 1


def handler(iface: NetworkInterface, ip_pac: IP, tcp_pac: TCP, raw_pac: scapy.Raw):
    k = reliability_coefficient(ip_pac, tcp_pac, raw_pac)

    print(f">>> Check {k}")
