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

    def create_prompt(self, prompt_name, prompt, user):
        result = self.cursor.execute('SELECT MAX(prompts_id) FROM prompts').fetchone()
        max_prompts_id = result[0]
        user_id = user[0]
        if max_prompts_id is not None:
            prompts_id = max_prompts_id + 1
        else:
            prompts_id = 0
        self.cursor.execute("INSERT into prompts (prompts_id, user_id, prompt_name, prompt, questions_count, "
                            "questions_correct) VALUES (?,?,?,?,?,?)",
                            (prompts_id, user_id, prompt_name, prompt, 0, 0))
        self.conn.commit()

        return True

    def delete_prompt(self, prompt_id):
        self.cursor.execute("DELETE FROM prompts WHERE prompts_id = ?", (prompt_id,))
        self.conn.commit()
        return True

    def prompts_info(self):
        result = self.cursor.execute('SELECT users.display_name, prompts.prompts_id, prompts.prompt_name FROM prompts '
                                     'INNER JOIN users ON prompts.user_id=users.user_id').fetchall()
        return result

    def show_single_prompt_info(self, prompt_id):
        result = self.cursor.execute('SELECT users.display_name, prompts.prompts_id, prompts.prompt_name FROM prompts '
                                     'INNER JOIN users ON prompts.user_id=users.user_id WHERE prompts.prompts_id = ?',
                                     (prompt_id,)).fetchone()
        return result
