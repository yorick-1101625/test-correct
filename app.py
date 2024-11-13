import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/vraag/<question_id>')
def scoring(question_id):
    return render_template('single-question.html')

if __name__ == "__main__":
    app.run(debug=True)