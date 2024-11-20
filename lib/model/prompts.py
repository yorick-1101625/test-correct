import sqlite3
from lib.model.database import Database

class Prompts:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_prompts(self):
        result = self.cursor.execute('SELECT * FROM prompts').fetchall()
        return result