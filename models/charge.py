from config import db

class Charge(db.Model):
    __tablename__ = 'charge'

    charge_code = db.Column(db.Integer, primary_key=True)
    crime_id = db.Column(db.Integer, db.ForeignKey('crime.crime_id'), primary_key=True)
    classification = db.Column(db.String(150))

    crime = db.relationship('Crime', back_populates='charges')