from config import db

class Crime(db.Model):
    __tablename__ = 'crime'

    crime_id = db.Column(db.Integer, primary_key=True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'))
    fine = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    payment_due_date = db.Column(db.DateTime)

    criminal = db.relationship('Criminal', backref=db.backref('crimes', lazy=True))