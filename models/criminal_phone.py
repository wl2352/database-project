from config import db

class CriminalPhone(db.Model):
    __tablename__ = 'criminal_phone'

    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)
    c_phone_number = db.Column(db.String(15), primary_key=True)

    # Relationship with Criminal Model
    criminal = db.relationship('Criminal', backref=db.backref('phones', lazy=True))

    def __repr__(self):
        return '<Phone %r>' % self.c_phone_number