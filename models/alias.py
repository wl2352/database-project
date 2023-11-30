from config import db

class Alias(db.Model):
    __tablename__ = 'alias'

    alias_name = db.Column(db.String(250), primary_key=True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.criminal_id'), primary_key=True)

    # Relationship with Criminal Model
    criminal = db.relationship('Criminal', backref=db.backref('aliases', lazy=True))

    def __repr__(self):
        return '<Alias %r>' % self.alias_name