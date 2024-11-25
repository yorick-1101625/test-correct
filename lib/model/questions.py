import sqlite3
from lib.model.database import Database

class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_single_question(self, questions_id):
        result = self.cursor.execute('SELECT * FROM questions WHERE questions_id = ?', (str(questions_id),)).fetchone()
        return result