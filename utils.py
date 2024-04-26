import socket
import sys
import scapy.all as scapy


def print_ifaces():
    for name, iface_obj in scapy.conf.ifaces.items():
        print(f"Name: \t{name}")
        print(f"Obj: \t{iface_obj}\n")


def print_local_ip():
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")


if __name__ == "__main__":
    cmd = sys.argv[-1].lower()

    if cmd == "ifaces":
        print_ifaces()
    elif cmd == "local_ip":
        print_local_ip()
    else:
        print(f"Неизвестная команда: {cmd}")
