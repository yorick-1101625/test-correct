import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('log-in.html')

if __name__ == "__main__":
    app.run(debug=True)