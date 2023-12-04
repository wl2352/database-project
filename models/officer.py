from config import db

class Officer(db.Model):
    __tablename__ = 'officer'

    badge_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    precinct = db.Column(db.Integer)
    status = db.Column(db.Boolean)

    crime_officers = db.relationship('CrimeOfficer', back_populates='officer', lazy=True, cascade='all, delete-orphan')
    phones = db.relationship('OfficerPhone', back_populates='officer', cascade='all, delete-orphan', lazy=True)

