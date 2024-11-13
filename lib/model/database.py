import sqlite3

# Weet niet of bronvermelding nog nodig is aangezien het nu gebaseerd is op code uit de casus
# L.C. (2023, 31 December). Build a To-Do List App Using Python Flask, Jinja2, and SQL. hashnode. Geraadpleegd op 13 November 2024 van https://lovelacecoding.hashnode.dev/build-a-to-do-list-app-using-python-flask-jinja2-and-sql
class Database:
    def __init__(self, db_path):
        # Locatie van het database bestand
        self.path = db_path

    def connect_db(self):
        # Maak verbinding met het database bestand
        conn = sqlite3.connect(self.path)
        # Geef het resultaat in een dictionary in plaats van een lijst
        conn.row_factory = sqlite3.Row
        # Maak een cursor object waarmee je SQL statements kan uitvoeren
        cursor = conn.cursor()
        return conn, cursor



# # Voer een SQL statement uit
# result = cursor.execute("SELECT count(*) AS teacher_count FROM teachers")
# # Nu niet nodig, maar stel dat dit een UPDATE statement was, dan had je nu moeten committen
# # conn.commit()
# number_of_teachers = result.fetchone()["teacher_count"]
# print(f"Er zijn {number_of_teachers} docenten in de database")
# # Sluit de verbinding met de database, is netjes, moet niet
# conn.close()