import flask
from flask import render_template

from lib.model.questions import Questions
from lib.model.prompts import Prompts

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/vraag/<questions_id>', methods=['GET', 'POST'])
def scoring(questions_id):
    questions_model = Questions()
    single_question = questions_model.read_single_question(questions_id)
    prompts_model = Prompts()
    prompts = prompts_model.read_prompts()
    return render_template('single-question.html', single_question=single_question, prompts=prompts)

if __name__ == "__main__":
    app.run(debug=True)