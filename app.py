import flask
from flask import render_template

from lib.model.questions import Questions
from lib.model.prompts import Prompts

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/overview')
def overview():
    questions_model = Questions()
    all_questions = questions_model.show_all_questions()
    return render_template('overview.html', all_questions=all_questions)

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