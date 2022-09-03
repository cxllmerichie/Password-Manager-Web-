from flask import render_template as render, Flask


app = Flask(__name__)


@app.route('/')
def template():
    return render('base.html')


@app.route('/home')
def home():
    return render('home.html')
