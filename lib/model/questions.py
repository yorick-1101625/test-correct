import sqlite3
from lib.model.database import Database

class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_ten_questions(self, offset):
        offset = 0 if offset < 0 else offset
        offset *= 10

        result = self.cursor.execute('SELECT * FROM questions LIMIT ? OFFSET ?', (10, offset)).fetchall()
        return result

    def show_filtered_questions(self, search_term, subject, indexed):
        if indexed == 'indexed':
            result = self.cursor.execute('SELECT * FROM questions WHERE question LIKE ? AND subject = ? AND taxonomy_bloom IS NOT NULL AND rtti IS NOT NULL',
                                         ("%"+search_term+"%", subject)).fetchall()
        elif indexed == 'not-indexed':
            result = self.cursor.execute('SELECT * FROM questions WHERE question LIKE ? AND subject = ? AND taxonomy_bloom IS NULL AND rtti IS NULL',
                ("%" + search_term + "%", subject)).fetchall()
        else:
            result = self.cursor.execute('SELECT * FROM questions WHERE question LIKE ? AND subject = ?',
                                         ("%" + search_term + "%", subject)).fetchall()
        return result

    def show_single_question(self, questions_id):
        result = self.cursor.execute('SELECT * FROM questions WHERE questions_id = ?', (str(questions_id),)).fetchone()
        return result