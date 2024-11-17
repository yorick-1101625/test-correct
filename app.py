import flask
from flask import render_template

from lib.model.questions import Questions

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/vraag/<questions_id>', methods=['GET', 'POST'])
def scoring(questions_id):
    question_model = Questions()
    single_question = question_model.read_single_question(questions_id)
    return render_template('single-question.html', single_question=single_question)

if __name__ == "__main__":
    app.run(debug=True)