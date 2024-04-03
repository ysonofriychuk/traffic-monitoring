import datetime
import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

        self.__cache_ip_clients = []
        self.__last_update = None

    def create_tables(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Таблица клиентов
        cursor.execute("""CREATE TABLE IF NOT EXISTS clients (
            ip varchar(15) PRIMARY KEY,
            mac varchar(17),
            is_visible bool default true,
            created_at date DEFAULT (CURRENT_TIMESTAMP)
        )
        """)

        # Логи подключения клиента к сети
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_last_time_in_network (
            ip varchar(15) REFERENCES clients(ip),
            time_action date DEFAULT (CURRENT_TIMESTAMP)
        )
        """)

        # Логи c коэффициентами достоверности
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_confidence_factor (
            ip varchar(15) REFERENCES clients(ip),
            result float NOT NULL,
            time_action date DEFAULT (CURRENT_TIMESTAMP)
        )
        """)

        connection.commit()
        connection.close()

    def add_clients_if_not_exist(self, rows: list[tuple[str, str]]):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.executemany(
            """INSERT INTO clients (ip, mac) VALUES (?, ?) ON CONFLICT DO UPDATE SET mac = excluded.mac""",
            rows
        )

        connection.commit()
        connection.close()

    def add_logs_last_time_in_network(self, ips: list[str]):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.executemany(
            """INSERT INTO logs_last_time_in_network (ip) VALUES (?)""",
            [(ip, ) for ip in ips]
        )

        connection.commit()
        connection.close()

    def add_log_confidence_factor(self, ip: str, result: float | str):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO logs_confidence_factor (ip, result) VALUES (?, ?)""",
            (ip, result)
        )

        connection.commit()
        connection.close()

    def get_ip_clients(self):
        if self.__last_update is not None:
            delta = datetime.datetime.now() - self.__last_update
            if delta.seconds < 60:
                return self.__cache_ip_clients, True

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT ip FROM clients""")

        self.__cache_ip_clients = [row[0] for row in cursor.fetchall()]
        self.__last_update = datetime.datetime.now()

        connection.close()

        return self.__cache_ip_clients, False
