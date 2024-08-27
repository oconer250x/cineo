from flask import Flask, render_template, url_for


cineoApp = Flask(__name__)

@cineoApp.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    cineoApp.run(debug=True,port=3300)