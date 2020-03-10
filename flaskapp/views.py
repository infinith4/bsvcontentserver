from flaskapp import app
from flask import render_template

@app.route('/')
def index():
    html = render_template('index.html', a = 'aaaa', title="HelloTitle")
    return html