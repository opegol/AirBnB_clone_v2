#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    """base route"""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """HBNB route"""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """route with variable"""
    return f"C {text.replace('_', ' ')}"

# @app.route("/python", defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def p_text(text='is_cool'):
    """route with variable"""
    return f"Python {text.replace('_', ' ')}"

@app.route("/number/<int:n>", strict_slashes=False)
def n_int(n):
    """route with integer variable"""
    return f"{n} is a number"

@app.route("/number_template/<int:n>", strict_slashes=False)
def num_tp_int(n):
    """route with integer variable and number template"""
    return render_template('5-number.html', num=n)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
