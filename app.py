from flask import Flask, render_template, request

from lib.model.questions import Questions
from lib.model.prompts import Prompts

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/overview/<offset>', methods=['GET', 'POST'])
def overview(offset):
    questions_model = Questions()
    offset = int(offset)
    if request.method == 'POST':
        search_term = str(request.form.get('search-term')) if request.form.get('search-term') else ""
        subject = str(request.form.get('subject'))
        indexed = 1 if request.form.get('indexed') else 0
        print(indexed)
        filtered_questions = questions_model.show_filtered_questions(search_term, subject, indexed)
        return render_template('overview.html', questions=filtered_questions, offset=offset)
    else:
        ten_questions = questions_model.show_ten_questions(offset=offset)
        return render_template('overview.html', questions=ten_questions, offset=offset)

@app.route('/vraag/<questions_id>', methods=['GET'])
def single_question_page(questions_id):
    # Show question
    questions_model = Questions()
    single_question = questions_model.show_single_question(questions_id)
    # Show all prompts
    prompts_model = Prompts()
    prompts = prompts_model.show_prompts()
    # Check if question exists
    if single_question is None:
        return "404: Question does not exist"
    else:
        return render_template('single-question.html', single_question=single_question, prompts=prompts)


if __name__ == "__main__":
    app.run(debug=True)