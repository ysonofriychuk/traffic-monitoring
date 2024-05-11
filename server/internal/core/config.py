import os
import socket

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "env.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

IPS_MASK = os.getenv("IPS_MASK_MONITORING")
IP_SERVER = os.getenv("IP_SERVER_MONITORING")
IFACE_NAME = os.getenv("IFACE_NAME_MONITORING")
PORT = os.getenv("PORT_MONITORING")

if not IP_SERVER:
    IP_SERVER = socket.gethostbyname(socket.gethostname())

if not PORT:
    PORT = "48888"

if not IPS_MASK:
    IPS_MASK = ".".join(IP_SERVER.split(".")[:-1]) + ".0/24"

FILTER_PAC_CLIENT = f"src host {IP_SERVER} and port {PORT} and tcp"
FILTER_PAC_SERVER = f"dst host {IP_SERVER} and port {PORT} and tcp"
