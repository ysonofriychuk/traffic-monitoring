Установка инструментов создания виртуального окружения

```shell
su root
apt update
apt -y upgrade
apt install -y python3-pip
apt install -y build-essential libssl-dev libffi-dev python3-dev
apt install -y python3-venv
```

Выполнение команд из Dockerfile

```shell
apt-get update 
apt-get -qq -y install gcc python3-dev tcpdump graphviz imagemagick swig libpcap-dev iputils-ping
```

Поднятие виртуального окружения Python

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Запуск необходимого скрипта

```shell
cd server
python3 server.py
```

```shell
cd client
python3 client.py
```