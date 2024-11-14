import flask
from flask import render_template
from lib.model.users import Users

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

@app.route('/vraag/<questions_id>')
def scoring(questions_id):
    return render_template('single-question.html', questions_id=questions_id)

@app.route('/login')
def login():
    users_model = Users()
    user_info = users_model.log_in()
    print(user_info)
    return render_template('log-in.html')

if __name__ == "__main__":
    app.run(debug=True)