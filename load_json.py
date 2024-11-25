import json
import sqlite3

connection = sqlite3.connect('databases/database.db')
cursor = connection.cursor()
cursor.execute('DELETE FROM questions')
connection.commit()


def load_questions(json_data):
    for questions in json_data:
        questions_id = questions['question_id']
        prompts_id = 0
        user_id = ''
        question = questions['question']
        subject = questions['vak']
        education_level = questions['onderwijsniveau']
        grade = questions['leerjaar']
        taxonomy_bloom = None
        rtti = None
        sql = '''INSERT INTO questions (questions_id, prompts_id, user_id, question, subject, education_level, grade, taxonomy_bloom, rtti) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        val = (questions_id, prompts_id, user_id, question, subject, education_level, grade, taxonomy_bloom, rtti)
        cursor.execute(sql, val)
    connection.commit()


def open_file():
    file = open('questions_extract.json')
    content = json.load(file)
    load_questions(content)
    file.close()
    connection.close()

open_file()