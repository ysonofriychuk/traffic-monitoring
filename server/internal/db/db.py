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
            variant varchar,
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

    def update_clients_info(self, rows: list[tuple[str, str, str]]):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(f"""UPDATE clients SET is_visible = false WHERE true""")

        cursor.executemany(
            """INSERT INTO clients (ip, mac, variant) 
            VALUES (?, ?, ?) 
            ON CONFLICT DO UPDATE SET mac = excluded.mac, is_visible = true, variant = excluded.variant""",
            rows
        )

        cursor.executemany(
            """INSERT INTO logs_last_time_in_network (ip) VALUES (?)""",
            [(row[0],) for row in rows]
        )

        connection.commit()
        connection.close()
        self.__last_update = None

    def add_log_confidence_factor(self, ip: str, result: float | str):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Выполняем вставку, только если IP существует в таблице clients
        cursor.execute("""
            INSERT INTO logs_confidence_factor (ip, result)
            SELECT ?, ?
            WHERE EXISTS (
                SELECT 1 FROM clients WHERE ip = ?
            )
        """, (ip, result, ip))

        connection.commit()
        connection.close()

    def get_clients_info(self, use_cache=True) -> list[tuple[str, str]]:
        if use_cache and self.__last_update is not None:
            delta = datetime.datetime.now() - self.__last_update
            if delta.seconds < 60:
                return self.__cache_ip_clients

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT ip, variant FROM clients WHERE is_visible""")

        self.__cache_ip_clients = cursor.fetchall()
        self.__last_update = datetime.datetime.now()

        connection.close()

        return self.__cache_ip_clients

    def hide_all_clients(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(f"""UPDATE clients SET is_visible = false WHERE true""")

        connection.commit()
        connection.close()
