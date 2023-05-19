import sqlite3
import datetime

class BotDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.cursor = self.db.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, msg):
        self.cursor.execute("INSERT INTO users (id, user_id, full_name, username, join_data) VALUES(?, ?, ?, ?, ?)", (
        len(self.cursor.execute("SELECT `id` FROM `users`").fetchall()), msg.from_user.id, msg.from_user.full_name, msg.from_user.username, datetime.datetime.now()))
        self.db.commit()

    def check_user_group(self, msg):
        user_info = self.cursor.execute("SELECT * FROM users WHERE user_id =?", (msg.from_user.id,))
        user_groups = user_info.fetchone()
        return user_groups

    def update_user_group(self, user_group, msg):
        self.cursor.execute(f"UPDATE users SET {user_group} = (?) WHERE user_id = (?)", (msg.text, msg.from_user.id))
        self.db.commit()