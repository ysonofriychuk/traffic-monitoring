# Система мониторинга пакетов

## Описание

Сервер отвечает за периодическую отправку пакетов 
клиентам внутри сети со сбором статистики о коэффициенте 
достоверности.

Клиент получает эти пакеты, рассчитывает коэффициент достоверности и 
отправляет ответ обратно серверу.

## Запуск и тестирование приложения

Перед началом работы убедитесь, что установлен Docker и Docker Compose, 
а также, проверьте `env.env` файлы с настройками.

Далее нужно запускать команды в зависимости от типа виртуальной машины (сервер/клиент)

Команды для работы с приложением:

### Сборка
  ```shell
  docker-compose -f server.docker-compose.yml build
  ```
  ```shell
  docker-compose -f client.docker-compose.yml build
  ```

### Запуск
  ```shell
  docker-compose -f server.docker-compose.yml up -d
  ```
  ```shell
  docker-compose -f client.docker-compose.yml up -d
  ```

### Выполнение ПО
  ```shell
  docker-compose -f server.docker-compose.yml exec scapy-server python server.py
  ```
  ```shell
  docker-compose -f client.docker-compose.yml exec scapy-client python client.py
  ```
  
### Остановка контейнеров
  ```shell
  docker-compose -f server.docker-compose.yml down
  ```
  ```shell
  docker-compose -f client.docker-compose.yml down
  ```