from lib.model.database import Database

class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_ten_not_indexed_questions(self, offset = 0):
        limit = 10
        result = self.cursor.execute(
            'SELECT DISTINCT * FROM questions WHERE taxonomy_bloom IS NULL OR rtti IS NULL LIMIT ? OFFSET ?',
            (limit, offset)).fetchall()
        return result

    def show_filtered_questions(self, subject, indexed, offset, search_term = ""):
        limit = 10
        if indexed == 'indexed':
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? AND taxonomy_bloom IS NOT NULL AND rtti IS NOT NULL AND exported = 0 LIMIT ? OFFSET ?',
                                         ("%"+search_term+"%", subject, limit, offset)).fetchall()
        elif indexed == 'not-indexed':
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? AND (taxonomy_bloom IS NULL OR rtti IS NULL) AND exported = 0 LIMIT ? OFFSET ?',
                                         ("%" + search_term + "%", subject, limit, offset)).fetchall()
        elif indexed == 'exported':
            result = self.cursor.execute('SELECT DISTINCT * FROM questions WHERE question LIKE ? AND subject = ? AND exported = 1 LIMIT ? OFFSET ?',
                                         ("%" + search_term + "%", subject, limit, offset)).fetchall()
        else:
            result = self.cursor.execute('SELECT DISTINCT  * FROM questions WHERE question LIKE ? AND subject = ? LIMIT ? OFFSET ?',
                                         ("%" + search_term + "%", subject, limit, offset)).fetchall()
        return result

    def show_single_question(self, questions_id):
        result = self.cursor.execute('SELECT * FROM questions WHERE questions_id = ?', (str(questions_id),)).fetchone()
        return result

    def get_indexed_questions(self):
        result = self.cursor.execute('SELECT DISTINCT * FROM questions WHERE taxonomy_bloom IS NOT NULL AND rtti IS NOT NULL AND exported = 0').fetchall()
        return result

    def set_exported(self, questions_id):
        result = self.cursor.execute('UPDATE questions SET exported = 1 WHERE questions_id = ?', (questions_id,))
        self.conn.commit()
        return result

    def update_question_stats(self, questions_id, prompts_id, taxonomy_bloom):
        self.cursor.execute('UPDATE questions SET prompts_id = ?, taxonomy_bloom = ? WHERE questions_id = ?',
                            (prompts_id, taxonomy_bloom, questions_id))
        self.conn.commit()
        return True