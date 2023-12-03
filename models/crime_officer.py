from config import db

class CrimeOfficer(db.Model):
    __tablename__ = 'crime_officer'

    crime_id = db.Column(db.Integer, db.ForeignKey('crime.crime_id'), primary_key=True)
    badge_no = db.Column(db.Integer, db.ForeignKey('officer.badge_no'), primary_key=True)

    officer = db.relationship('Officer', back_populates='crime_officers')
    crime = db.relationship('Crime', back_populates='crime_officers')
