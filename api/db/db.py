import os
import psycopg2
import sqlite3

from dotenv import load_dotenv

from models.user import User
from dto.userDTO import UserDTO


load_dotenv()


class DataBase:
    def __init__(self, file) -> None:
        self.file = file
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.connect()

    def connect(self) -> None:
        # TODO prod
        # self.conn = psycopg2.connect(
        #     dbname=self.dbname,
        #     user=self.user,
        #     password=self.password,
        #     host=self.host,
        #     port=self.port
        # )
        # TODO dev
        self.conn = sqlite3.connect(self.file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_user(self, user: User) -> int:
        username = user.username or "null"
        chatid = user.chatID
        self.cursor.execute("INSERT INTO users (userName, telegramChatId) VALUES (?, ?)", (username, chatid))
        self.conn.commit()
        self.cursor.execute("SELECT last_insert_rowid() AS userId")
        user_id = self.cursor.fetchone()[0]
        return user_id
    
    def get_user(self, user_id: int) -> User:
        self.cursor.execute("SELECT userName, telegramChatId FROM users WHERE telegramChatId = ?", (user_id,))
        res = self.cursor.fetchall()
        if res:
            row = res[0]
            return User(username=row[0], chatID=row[1])
        return None
    
    def get_users(self):
        self.cursor.execute("SELECT userId, userName, telegramChatId FROM users")
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            user = UserDTO(row[0], row[1], row[2])
            users.append(user)
        return [user.to_dict() for user in users]

    

    
db = DataBase('test.db')