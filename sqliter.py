import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_message(self, a):
        """Добавляем новое сообщение"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `RN_DATA` (`number_zak`, `Title`, `organizer`, `date_publication`, `end_date`, `summing_results`, `additionally`, `customer`, `customer_try`, `contact_person`, `href`) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (a['number_zak'], a['Title'], a['organizer'], a['date_publication'], a['end_date'], a['summing_results'],
                 a['additionally'], a['customer'], a['customer_try'], a['contact_person'], a['href']))

    # Созадние таблицы
    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS RN_DATA(
            number_zak TEXT,
            Title TEXT,
            organizer TEXT,
            date_publication TEXT,
            end_date TEXT,
            summing_results TEXT,
            additionally TEXT,
            customer TEXT,
            customer_try TEXT,
            contact_person TEXT,
            href TEXT);
            """
        )
        self.connection.commit()

    # Получаем список всех таблиц
    def all_table(self):
        return self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    def allpost_exists(self, number_zak):
        """Проверяем, есть ли уже сообщение в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `RN_DATA` WHERE `number_zak` = ?', (number_zak,)).fetchall()
            return bool(len(result))