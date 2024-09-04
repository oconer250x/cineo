from flask import Flask, render_template, url_for

cineo = Flask(__name__)

@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/signin')
def signin():
    return render_template('signin.html')

@cineo.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    cineo.run(debug=True,port=3300)
