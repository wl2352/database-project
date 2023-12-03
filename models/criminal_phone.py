from config import db

class CriminalPhone(db.Model):
    __tablename__ = 'criminal_phone'

    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)
    c_phone_number = db.Column(db.String(15), primary_key=True)

    criminal = db.relationship('Criminal', back_populates='phones')
