import sqlite3
import pytest
from fastapi.testclient import TestClient

from Users import users_db
from Users.Models import User
from App.app import authenticate_user
from main import app

class TestUM:
    def setup_class(cls):
        cls.database = 'users.db'
        cls.table = 'test'
        cls.username = "test_username"
        cls.password = "test_password"
        cls.spending = 100.0
        cls.cashback = 5.0
        cls.cashback_level = "GOLD"
        cls.client = TestClient(app)
        users_db.create_user(cls.username, cls.password, cls.spending, cls.cashback, cls.cashback_level, table=cls.table)
        

    def test_authenticate_user(self):
        user = authenticate_user(self.username, self.password, table=self.table)
        assert isinstance(user, User)
        assert user.username == self.username
        assert user.password == self.password
        assert user.spending == self.spending
        assert user.cashback == self.cashback
        assert user.cashback_level == self.cashback_level

        false_user = authenticate_user(self.username, "wrong_password", table=self.table)
        assert (false_user is False)

    def test_get_token(self):
        response = self.client.post("/token", params={"table": self.table}, data={"username": self.username, "password": self.password})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_get_token_fail(self):
        response = self.client.post("/token", params={"table": self.table}, data={"username": self.username, "password": "wrong_password"})
        assert response.status_code == 401

    def test_read_spending_authenticated(self):
        login_response = self.client.post("/token", params={"table": self.table}, data={"username": self.username, "password": self.password})
        token = login_response.json()["access_token"]
        response = self.client.get("/spending", headers={"Authorization": f"Bearer {token}"}, params={"table": self.table})
        assert response.status_code == 200
        assert "spending(RUB)" in response.json() 
        assert "cashback(%)" in response.json() 
        assert "cashback level" in response.json()

    def test_read_spending_unauthenticated(self):
        response = self.client.get("/spending")
        assert response.status_code == 401