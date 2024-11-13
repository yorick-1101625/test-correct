import sqlite3

# L.C. (2023, 31 December). Build a To-Do List App Using Python Flask, Jinja2, and SQL. hashnode. Geraadpleegd op 13 November 2024 van https://lovelacecoding.hashnode.dev/build-a-to-do-list-app-using-python-flask-jinja2-and-sql
class Database:
    def __init__(self, db_path):
        self.path = db_path

    def connect_db(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        return con, cursor