import flask
from flask import render_template
from lib.model.users import Task

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    database = Task()
    test = database.log_in()
    return render_template('log-in.html')

if __name__ == "__main__":
    app.run(debug=True)