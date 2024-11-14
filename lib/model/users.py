from lib.model.database import Database

class Users():
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def log_in(self):
        result = self.cursor.execute('SELECT * FROM users').fetchall()
        return result