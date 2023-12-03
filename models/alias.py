from config import db

class Alias(db.Model):
    __tablename__ = 'alias'

    alias_name = db.Column(db.String(250), primary_key=True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)

    criminal = db.relationship('Criminal', back_populates='aliases')