import json
import sqlite3

from lib.model.database import Database

class Json:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()


    def load_questions(self, json_data):
        for questions in json_data:
            questions_id = questions['question_id']
            prompts_id = None
            user_id = None
            question = questions['question']
            subject = questions['vak']
            education_level = questions['onderwijsniveau']
            grade = questions['leerjaar']
            taxonomy_bloom = None
            rtti = None
            sql = '''INSERT INTO questions (questions_id, prompts_id, user_id, question, subject, education_level,
             grade, taxonomy_bloom, rtti) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            val = (questions_id, prompts_id, user_id, question, subject, education_level, grade, taxonomy_bloom, rtti)
            self.cursor.execute(sql, val)
        self.conn.commit()


    def open_file(self, file):
        content = json.load(file)
        self.load_questions(content)
        self.conn.close()
        return True