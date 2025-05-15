import json
import os
import random

USER_FILE = "users.json"

class User:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def increase_balance(self):
        if self.balance < 20000:
            increase = random.randint(1000, 3000)
            self.balance = min(self.balance + increase, 20000)

    def to_dict(self):
        return {"password": self.password, "balance": self.balance}

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def login_or_register(username, password):
    users = load_users()

    if username in users:
        if users[username]["password"] == password:
            user = User(username, password, users[username]["balance"])
            user.increase_balance()
            users[username]["balance"] = user.balance
            save_users(users)
            return user
        else:
            raise ValueError("Falsches Passwort!")
    else:
        # Registrierung
        user = User(username, password)
        user.increase_balance()
        users[username] = user.to_dict()
        save_users(users)
        return user
