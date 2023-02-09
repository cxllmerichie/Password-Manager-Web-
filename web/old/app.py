from flask import render_template as render, Flask


app = Flask(__name__)


@app.route('/')
def template():
    return render('base.html')


@app.route('/home')
def home():
    return render('home.html')


@app.route('/profile')
def profile():
    return render('profile.html')


@app.route('/security')
def security():
    return render('security.html')
