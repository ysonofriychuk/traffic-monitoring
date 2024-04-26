import scapy.all as scapy


def handler(raw_pac: scapy.Raw):
    raw_load: bytes = raw_pac.load
    raw_load_str: str = raw_load.decode("utf-8")

    return raw_load_str.replace("ping->", "")
