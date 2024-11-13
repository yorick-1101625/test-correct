import flask
from flask import render_template
from task import Task

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/vraag/<question_id>')
def scoring(question_id):
    return render_template('single-question.html', questions_id=questions_id)

@app.route('/login', methods=['POST'])
def login():
    database = Task()
    test = database.log_in()
    return render_template('log-in.html')



if __name__ == "__main__":
    app.run(debug=True)