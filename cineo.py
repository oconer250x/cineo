from flask import Flask

cineoApp = Flask(__name__)

@cineoApp.route('/')
def home():
    return '<h1>me gustan las chichis JABADABADOO</h1>'

if __name__ == "__main__":
    cineoApp.run(debug=True,port=3300)