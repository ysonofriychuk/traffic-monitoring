#!/bin/sh

# Обновление списка пакетов
apt-get update

# Установка пакетов, необходимых для установки Docker
apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    gcc \
    python3-dev \
    tcpdump \
    graphviz \
    imagemagick \
    swig \
    libpcap-dev \
    iputils-ping \
    python3-pip


# Добавление официального ключа GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Добавление репозитория Docker
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Установка Docker
apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io

# Удаление пакетов, которые больше не нужны
apt-get -y autoremove

# Удаление пакетов, используемых в установке Docker
apt-get -y purge \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Очистка кэша пакетов
apt-get clean

# Удаление временных файлов
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*