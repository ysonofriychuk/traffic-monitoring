import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "env.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

IP_SERVER = os.getenv("IP_SERVER_MONITORING")
IFACE_NAME = os.getenv("IFACE_NAME_MONITORING")
PORT = os.getenv("PORT_MONITORING")

if not PORT:
    PORT = "48888"

FILTER_PAC_CLIENT = f"src host {IP_SERVER} and port {PORT} and tcp"

if not IP_SERVER:
    FILTER_PAC_CLIENT = f"port {PORT} and tcp"
