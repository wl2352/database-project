from config import db

class OfficerPhone(db.Model):
    __tablename__ = 'officer_phone'

    badge_no = db.Column(db.Integer, db.ForeignKey('officer.badge_no'), primary_key=True)
    o_phone_number = db.Column(db.String(15), primary_key=True)

    officer = db.relationship('Officer', backref=db.backref('phones', lazy=True))