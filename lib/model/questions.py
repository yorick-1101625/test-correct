import sqlite3
from lib.model.database import Database

class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_ten_not_indexed_questions(self, offset = 0):
        result = self.cursor.execute(
            'SELECT DISTINCT * FROM questions WHERE taxonomy_bloom IS NULL OR rtti IS NULL LIMIT ? OFFSET ?',
            (10, offset)).fetchall()
        return result

    def show_filtered_questions(self, subject, indexed, offset, search_term = ""):
        if indexed == 'indexed':
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? AND taxonomy_bloom IS NOT NULL AND rtti IS NOT NULL LIMIT ? OFFSET ?',
                                         ("%"+search_term+"%", subject, 10, offset)).fetchall()
        elif indexed == 'not-indexed':
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? AND taxonomy_bloom IS NULL OR rtti IS NULL LIMIT ? OFFSET ?',
                ("%" + search_term + "%", subject, 10, offset)).fetchall()
        else:
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? LIMIT ? OFFSET ?',
                                         ("%" + search_term + "%", subject, 10, offset)).fetchall()
        return result

    def show_single_question(self, questions_id):
        result = self.cursor.execute('SELECT * FROM questions WHERE questions_id = ?', (str(questions_id),)).fetchone()
        return result