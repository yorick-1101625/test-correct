from lib.model.database import Database


class Users():
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_users(self):
        result = self.cursor.execute('SELECT * FROM users').fetchall()
        return result

    def create_users(self, display_name, login, password):
        result = self.cursor.execute('SELECT MAX(user_id) FROM users').fetchone()
        max_user_id = result[0]
        if max_user_id is not None:
            user_id = max_user_id + 1
        else:
            user_id = 0
        self.cursor.execute("INSERT into users (user_id, login, password, display_name, is_admin) VALUES (?,?,?,?,?)",
                            (user_id, login, password, display_name, 0))
        self.conn.commit()

        return True