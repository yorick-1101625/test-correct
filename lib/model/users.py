from lib.model.database import Database
from hashlib import sha256

class Users():
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()


    def show_users(self):
        result = self.cursor.execute('SELECT * FROM users').fetchall()
        return result


    def show_single_user(self, user_id):
        result = self.cursor.execute('SELECT * FROM users WHERE user_id = ?',
                                     (user_id,)).fetchone()
        return result


    def admin_check(self, user_id):
        active_user = self.show_single_user(user_id)
        if active_user is None:
            return False

        user_is_admin = active_user['is_admin']
        if user_is_admin == 1:
            return True
        else:
            return False


    def create_users(self, display_name, login, password, is_admin):
        password = hash_password(password)
        self.cursor.execute("INSERT into users (login, password, display_name, is_admin) VALUES (?,?,?,?)",
                            (login, password, display_name, is_admin))
        self.conn.commit()

        return True


    def edit_users(self, display_name, login, password, user_id, is_admin):
        if password:
            password = hash_password(password)
            self.cursor.execute('UPDATE users SET login = ?, password = ?, display_name = ?, is_admin = ? WHERE '
                                'user_id = ?',
                                (login, password, display_name, is_admin, user_id))
        else:
            self.cursor.execute('UPDATE users SET login = ?, display_name = ?, is_admin = ? WHERE user_id = ?',
                (login, display_name, is_admin, user_id))
        self.conn.commit()
        return True


    def delete_users(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE user_id = ?',
                            user_id)
        self.conn.commit()
        return True


    def log_in(self, email, password):
        password = hash_password(password)
        # Fetch the user record based on the username
        self.cursor.execute('SELECT * FROM users WHERE login = ?', (email,))
        user = self.cursor.fetchone()

        # Check if user exists and password matches
        if user and password == user['password']:
            return user  # Login successful
        return False  # Login failed


def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()
