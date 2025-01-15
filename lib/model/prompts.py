from lib.model.database import Database

class Prompts:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()


    def show_single_prompt(self, prompts_id):
        result = self.cursor.execute('SELECT * FROM prompts WHERE prompts_id = ?', (prompts_id,)).fetchone()
        return result


    def show_prompts_per_category(self, category):
        result = self.cursor.execute('SELECT * FROM prompts WHERE prompt_category = ?', (category,)).fetchall()
        return result


    def create_prompt(self, prompt_name, prompt, user_id, prompt_category):
        self.cursor.execute("INSERT into prompts (user_id, prompt_name, prompt, questions_count,"
                            "questions_correct, prompt_category) VALUES (?,?,?,?,?,?)",
                            (user_id, prompt_name, prompt, 0, 0, prompt_category))
        self.conn.commit()

        return True


    def delete_prompt(self, prompt_id):
        self.cursor.execute("DELETE FROM prompts WHERE prompts_id = ?", (prompt_id,))
        self.conn.commit()
        return True


    def prompts_info(self):
        result = self.cursor.execute('SELECT * FROM prompts '
                                     'INNER JOIN users ON prompts.user_id=users.user_id').fetchall()
        return result


    def show_single_prompt_info(self, prompt_id):
        result = self.cursor.execute('SELECT users.display_name, prompts.prompts_id, prompts.prompt_name FROM prompts '
                                     'INNER JOIN users ON prompts.user_id=users.user_id WHERE prompts.prompts_id = ?',
                                     (prompt_id,)).fetchone()
        return result


    def get_prompt_stats(self, prompt_id):
        result = self.cursor.execute('SELECT questions_count, questions_correct FROM prompts WHERE prompts_id = ?',
                                     (prompt_id,)).fetchone()
        return result


    def update_prompt_stats(self, prompts_id, changed_by_user):
        stats = self.get_prompt_stats(prompts_id)
        questions_count = stats['questions_count'] + 1
        questions_correct = stats['questions_correct']
        if not changed_by_user:
            questions_correct += 1

        self.cursor.execute('UPDATE prompts SET questions_count = ?, questions_correct = ? WHERE prompts_id = ?',
                            (questions_count, questions_correct, prompts_id))
        self.conn.commit()
        return True


    def structure_bloom_prompt(self, prompt):
        structured_prompt = prompt + """
        Geef het antwoord in een RFC8259 JSON met de volgende opmaak, waar je niet van mag afwijken.
        "categorie" MOET een van de volgende categorieën zijn: "Onthouden", "Begrijpen", "Toepassen", "Analyseren", 
        "Evalueren" en "Creëren"
        {
           "categorie": "het gekozen niveau van Bloom",
           "uitleg": "uitleg waarom dit niveau van toepassing is"
        }
        """
        return structured_prompt


    def structure_rtti_prompt(self, prompt):
        structured_prompt = prompt + """
        Geef het antwoord in een RFC8259 JSON met de volgende opmaak, waar je niet van mag afwijken.
        "categorie" MOET een van de volgende categorieën zijn: "R", "T1", "T2", "I".
        {
           "categorie": "het gekozen niveau van RTTI",
           "uitleg": "uitleg waarom dit niveau van toepassing is"
        }
        """
        return structured_prompt
