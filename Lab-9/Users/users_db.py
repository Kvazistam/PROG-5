import sqlite3

from Users.Models import User

# В файле находятся функции для взаимодействия с базой данных, в основном используются для отладки и юнит тестов


def get_user(username, table= "users", database="users.db"):
    """Находит пользователя в users.db и возвращает объект класса User"""
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()
    if user_record:
        return User(user_record['username'], user_record['password'], user_record['spending'],
                    user_record['cashback'], user_record['cashback_level'])
    return False

def create_user(username, password, spending, cashback = None, cashback_level = None, table="users",  database = "users.db"):
    """Создает пользователя в users.db с переданными параметрами"""
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY, "
                           "username TEXT NOT NULL,"
                           "password TEXT  NOT NULL,"
                           "spending REAL NOT NULL,"
                           "cashback REAL, "
                           "cashback_level TEXT CHECK (cashback_level IN ('GOLD', 'SILVER', 'PLATINUM')));")
    cursor.execute(
            f"INSERT INTO {table}(username, password, spending, cashback, cashback_level) VALUES(?, ?, "
            "?, ?, ?);", (username, password, spending, cashback, cashback_level))
    conn.commit()
    conn.close()

def delete_user(username, table="users",  database = "users.db"):
    """Удаляет пользователя в users.db"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def update_user(username, password=None, spending=None, cashback=None, cashback_level=None, table="users",  database = "users.db"):
    """Обновляет данные пользователя в users.db"""
    conn = sqlite3.connect( database)
    cursor = conn.cursor()
    if password:
        cursor.execute(f"UPDATE {table} SET password = ? WHERE username = ?", (password, username))
    if spending:
        cursor.execute(f"UPDATE {table} SET spending = ? WHERE username = ?", (spending, username))
    if cashback:
        cursor.execute(f"UPDATE {table} SET cashback = ? WHERE username = ?", (cashback, username))
    if cashback_level:
        cursor.execute(f"UPDATE {table} SET cashback_level = ? WHERE username = ?", (cashback_level, username))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_user("Nikita", "12345", 10)
    create_user("Nikita1", "12345", 1000)
    create_user("Nikita2", "12345789", 10000000)

