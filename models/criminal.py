from config import db

class Criminal(db.Model):
    __tablename__ = 'criminal'

    criminal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    violent_status = db.Column(db.Boolean)
    probation_status = db.Column(db.Boolean)

    # aliases, addresses, phones, and crimes will be deleted along with the criminal
    aliases = db.relationship('Alias', back_populates='criminal', cascade='all, delete-orphan', lazy=True)
    addresses = db.relationship('Address', back_populates='criminal', cascade='all, delete-orphan', lazy=True)
    phones = db.relationship('CriminalPhone', back_populates='criminal', cascade='all, delete-orphan', lazy=True)
    sentences = db.relationship('Sentence', back_populates='criminal', cascade='all, delete-orphan', lazy=True)
    crimes = db.relationship('Crime', back_populates='criminal', cascade='all, delete-orphan', lazy=True)

    
    def serialize(self):
        return {
            'criminal_id': self.criminal_id,
            'name': self.name,
            'violent_status': self.violent_status,
            'probation_status': self.probation_status
        }