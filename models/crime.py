from config import db

class Crime(db.Model):
    __tablename__ = 'crime'

    crime_id = db.Column(db.Integer, primary_key=True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'))
    fine = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    payment_due_date = db.Column(db.DateTime)
    court_fee = db.Column(db.Float)

    # appeals, crime_officers, and appeals will be deleted along with the crime
    # officers wont be deleted since officer is the parent of this relationship
    criminal = db.relationship('Criminal', back_populates='crimes')
    appeals = db.relationship('Appeal', back_populates='crime', lazy=True, cascade='all, delete-orphan')
    crime_officers = db.relationship('CrimeOfficer', back_populates='crime', lazy=True, cascade='all, delete-orphan')
    charges = db.relationship('Charge', back_populates='crime', lazy=True, cascade='all, delete-orphan')