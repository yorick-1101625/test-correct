from lib.model.database import Database

class Users():
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def log_in(self):
        result = self.cursor.execute('SELECT * FROM users').fetchall()
        return result

    def log_in(self, username, password):
        self.cursor.execute('''SELECT login, password FROM users''')
        credentials = self.cursor.fetchall()
        for credential in credentials:
            if username != credential[0] and password != credentials[1]:
                print('FOUT')
            else:
                print('GOED')