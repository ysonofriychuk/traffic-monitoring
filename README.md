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

TODO: добавить схему обмена

## Запуск и тестирование приложения

Перед началом работы убедитесь, что установлен Docker и Docker Compose, 
а также, проверьте [config.py](src%2Finternal%2Fcore%2Fconfig.py) файл с настройками.

Команды для работы с приложением:

### Сборка образа
  ```shell
  docker-compose build
  ```

### Запуск контейнеров
  ```shell
  docker-compose up -d
  ```

### Выполнение ПО на клиентах
  ```shell
  docker-compose exec scapy-client-1 python client.py
  ```
  ```shell
  docker-compose exec scapy-client-2 python client.py
  ```

### Выполнение ПО на сервере
  ```shell
  docker-compose exec scapy-server python server.py
  ```
  
### Остановка контейнеров
  ```shell
  docker-compose down
  ```
