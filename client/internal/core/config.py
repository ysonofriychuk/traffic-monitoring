import os

IP_SERVER = os.getenv("IP_SERVER_MONITORING")

IFACE_NAME = os.getenv("IFACE_NAME_MONITORING")
PORT = os.getenv("PORT_MONITORING")

if not PORT:
    PORT = "48888"

if not IFACE_NAME:
    IFACE_NAME = "eth0"

FILTER_PAC_CLIENT = f"src host {IP_SERVER} and port {PORT} and tcp"

if not IP_SERVER:
    FILTER_PAC_CLIENT = f"port {PORT} and tcp"
