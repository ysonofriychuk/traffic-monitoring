# Система мониторинга пакетов

## Описание

Сервер отвечает за периодическую отправку пакетов 
клиентам внутри сети со сбором статистики о коэффициенте 
достоверности.

Клиент получает эти пакеты, рассчитывает коэффициент достоверности и 
отправляет ответ обратно серверу.

## Запуск и тестирование приложения

Перед началом работы убедитесь, что установлен Docker и Docker Compose, 
а также, проверьте `env.env` файлы с настройками, которые находятся в директориях
`server` и `client`. Необходимо настраивать только тот файл, который будет использоваться
в виртуальной машине.

Обратите внимание, что можно не указывать `IFACE_NAME_MONITORING`, тогда нужно будет его выбрать
после запуска ПО в контейнере. Также, `IPS_MASK_MONITORING` можно пропустить, тогда она автоматически
построится на основе IP сервера. Все остальные параметры указывать обязательно.

Логи хранятся в директориях по путям `server/logs` и `client/logs`. База данных, заполняемая сервером,
хранится в `server/db`.

Ниже перечислены команды для запуска в зависимости от типа виртуальной машины (сервер/клиент).

### Сервер

#### Сборка
  ```shell
  docker-compose -f server.docker-compose.yml build
  ```

#### Запуск
  ```shell
  docker-compose -f server.docker-compose.yml up -d
  ```

#### Выполнение ПО
  ```shell
  docker-compose -f server.docker-compose.yml exec scapy-server python server.py
  ```
  
#### Остановка контейнеров
  ```shell
  docker-compose -f server.docker-compose.yml down
  ```

### Клиент

#### Сборка
  ```shell
  docker-compose -f client.docker-compose.yml build
  ```

#### Запуск
  ```shell
  ```shell
  docker-compose -f client.docker-compose.yml up -d
  ```

#### Выполнение ПО
  ```shell
  docker-compose -f client.docker-compose.yml exec scapy-client python client.py
  ```
  
#### Остановка контейнеров
  ```shell
  docker-compose -f client.docker-compose.yml down
  ```