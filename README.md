# Система мониторинга пакетов

## Описание

Проект представлен двумя основными файлами:
- [client.py](src%2Fclient.py)
- [server.py](src%2Fserver.py)

Сервер отвечает за периодическую отправку пакетов 
клиентам внутри сети со сбором статистики о коэффициенте 
достоверности.

Клиент получает эти пакеты, рассчитывает коэффициент достоверности и 
отправляет ответ обратно серверу.

## Начало работы

Перед началом работы убедитесь, что установлен Docker и Docker Compose.

Для запуска проекта необходимо собрать и запустить контейнеры из [docker-compose.yml](docker-compose.yml).

```shell
# Сборка
docker-compose build
```

```shell
# Запуск
docker-compose up -d
```

Для остановки контейнеров и освобождения ресурсов выполните:
```shell
docker-compose down
```

Когда контейнеры запущены необходимо зайти в них и выполнить script на Python.

Клиент 1
```shell
docker-compose exec scapy-client-1 python client.py
```

Клиент 2
```shell
docker-compose exec scapy-client-2 python client.py
```

Сервер:
```shell
docker-compose exec scapy-server python server.py
```

Программы общаются через интерфейс `eth0`