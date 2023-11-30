from config import db

class Address(db.Model):
    __tablename__ = 'address'

    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)
    street_address = db.Column(db.String(150), primary_key=True)
    city = db.Column(db.String(50))
    state = db.Column(db.String(13))
    zip_code = db.Column(db.Integer, primary_key=True)

    # Relationship with Criminal Model
    criminal = db.relationship('Criminal', backref=db.backref('addresses', lazy=True))

    def __repr__(self):
        return '<Address %r>' % self.street_address