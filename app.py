from flask import Flask, render_template
from config import db
from models.criminal import Criminal
from models.alias import Alias

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
db.init_app(app)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/criminal')
def criminal_page():
    return render_template('criminal.html')

@app.route('/criminals')
def list_of_criminals():
    criminals = Criminal.query.all()
    return render_template('criminals.html', criminals=criminals)

@app.route('/criminal/<int:id>', methods=['GET'])
def get_criminal(id):
    criminal = Criminal.query.get(id)
    return render_template('criminal.html', criminal=criminal)

if __name__ == '__main__':
    app.run(debug=True, port='3000')