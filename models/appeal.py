from config import db

class Appeal(db.Model):
    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, primary_key=True)
    crime_id = db.Column(db.Integer, db.ForeignKey('crime.crime_id'))
    filing_date = db.Column(db.Date)
    hearing_date = db.Column(db.Date)
    appeal_status = db.Column(db.String(150))