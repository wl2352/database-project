from config import db

class Sentence(db.Model):
    __tablename__ = 'sentences'

    sentence_id = db.Column(db.Integer, primary_key=True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    num_violations = db.Column(db.Integer)
    type = db.Column(db.String(150))

    criminal = db.relationship('Criminal', back_populates='sentences')