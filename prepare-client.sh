#!/bin/sh

apt-get update
apt-get -y install gcc python3-dev tcpdump graphviz imagemagick swig libpcap-dev iputils-ping

rm -r ./server
rm -r ./docker
rm docker-compose.yml

python3 -m venv venv

# shellcheck disable=SC2039
source venv/bin/activate
pip install -r requirements.txt