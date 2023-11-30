from config import db

class Officer(db.Model):
    __tablename__ = 'officer'

    badge_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    precinct = db.Column(db.Integer)
    status = db.Column(db.Boolean)