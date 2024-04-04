IPS_MASK = "10.5.0.0/24"
IP_SERVER = "10.5.0.10"
IFACE_NAME = "eth0"
PORT = "48888"

FILTER_PAC_CLIENT = f"src host {IP_SERVER} and port {PORT} and tcp"
FILTER_PAC_SERVER = f"dst host {IP_SERVER} and port {PORT} and tcp"
