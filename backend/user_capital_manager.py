import json
import os
import random

USER_FILE = "users.json"
SESSION_FILE = "session.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_current_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return json.load(f).get("username")

def set_current_user(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def augment_user_capital(username):
    users = load_users()
    if username not in users:
        users[username] = {"capital": 0}
    increase = random.randint(1000, 3000)
    current = users[username]["capital"]
    new_capital = min(current + increase, 20000)
    users[username]["capital"] = new_capital
    save_users(users)
    return new_capital

def get_user_capital(username):
    users = load_users()
    return users.get(username, {}).get("capital", 0)
