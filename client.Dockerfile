FROM python:3.11
MAINTAINER Yaroslav Onofrijchuk "ysonofriychuk@bk.ru"

RUN apt-get update && \
    apt-get -qq -y install \
    gcc python3-dev tcpdump graphviz imagemagick \
    swig libpcap-dev iputils-ping && \
    apt-get clean

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /scapy/src
ENTRYPOINT ["bash"]
