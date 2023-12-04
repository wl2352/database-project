from config import db

class Address(db.Model):
    __tablename__ = 'address'

    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)
    street_address = db.Column(db.String(150), primary_key=True)
    city = db.Column(db.String(50))
    state = db.Column(db.String(13))
    zip_code = db.Column(db.Integer, primary_key=True)

    criminal = db.relationship('Criminal', back_populates='addresses')
