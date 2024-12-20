import sqlite3
from passlib.context import CryptContext
from enum import Enum


class Cashback_levels(Enum):
    SILVER = 5
    GOLD = 10
    PLATINUM = 15


class User:
    """Класс пользователя для более удобного представления данных из бд"""

    def __init__(self, username, password, spending: int, cashback = None, cashback_level = None):
        self.username = username
        self.password = password
        self.spending = spending
        if cashback_level:
            self.cashback_level = cashback_level
        else:
            cashback_level = self.count_cashback(spending)
            self.cashback_level = cashback_level.name
        if cashback:
            self.cashback = cashback
        else:
            self.cashback = cashback_level.value
    def __str__(self):
        return f"username: {self.username} password: {self.password}, cashback: {self.cashback} cashback_level: {self.cashback_level.name}"
        
        

    @staticmethod
    def count_cashback(spending: int) -> Cashback_levels:
        if spending < 10**3:
            return Cashback_levels.SILVER
        elif 10**3 <= spending < 10**4:
            return Cashback_levels.GOLD
        else:
            return Cashback_levels.PLATINUM

    def verify_password(self, password):
        return self.password == password

    def as_dict(self):
        return {
            "username": self.username,
            "spending": self.spending,
            "cashback_level": self.cashback_level,
            "cashback": self.cashback
        }
