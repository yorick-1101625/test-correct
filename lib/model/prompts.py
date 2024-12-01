import sqlite3
from lib.model.database import Database

class Prompts:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_single_prompt(self, prompts_id):
        result = self.cursor.execute('SELECT * FROM prompts WHERE prompts_id = ?', (prompts_id,)).fetchone()
        return result

    def show_prompts(self):
        result = self.cursor.execute('SELECT * FROM prompts').fetchall()
        return result

    def create_prompt(self, prompt_name, prompt):
        self.cursor.execute("INSERT into prompts (prompts_id, user_id, prompt_name, prompt, questions_count, questions_correct) VALUES (?,?,?,?,?,?)",
                            (0, 0, prompt_name, prompt, 0, 0))
        self.conn.commit()

        return True