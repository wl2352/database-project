from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/criminal')
def criminal_page():
    return render_template('criminal.html')

if __name__ == '__main__':
    app.run(debug=True, port='3000')