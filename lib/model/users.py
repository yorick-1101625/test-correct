from lib.model.database import Database


class Users():
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def show_users(self):
        result = self.cursor.execute('SELECT * FROM users').fetchall()
        return result

    def show_single_user(self, user_id):
        result = self.cursor.execute('SELECT * FROM users WHERE user_id = ?',
                                     user_id).fetchone()
        return result

    def create_users(self, display_name, login, password, is_admin):
        result = self.cursor.execute('SELECT MAX(user_id) FROM users').fetchone()
        max_user_id = result[0]
        if max_user_id is not None:
            user_id = max_user_id + 1
        else:
            user_id = 0
        self.cursor.execute("INSERT into users (user_id, login, password, display_name, is_admin) VALUES (?,?,?,?,?)",
                            (user_id, login, password, display_name, is_admin))
        self.conn.commit()

        return True

    def edit_users(self, display_name, login, password, user_id, is_admin):
        self.cursor.execute('UPDATE users SET login = ?, password = ?, display_name = ?, is_admin = ? WHERE user_id = ?',
                            (login, password, display_name, is_admin, user_id))
        self.conn.commit()
        return True

    def delete_users(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE user_id = ?',
                            user_id)
        self.conn.commit()
        return True

    def log_in(self, email, password):
        # Fetch the user record based on the username
        self.cursor.execute('SELECT login, password FROM users WHERE login = ?', (email,))
        user = self.cursor.fetchone()

        # Check if user exists and password matches
        if user and password == user[1]:  # Direct string comparison for passwords
            return True  # Login successful
        return False  # Login failed


