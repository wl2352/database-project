from config import db

class Criminal(db.Model):
    __tablename__ = 'criminal'

    criminal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    violent_status = db.Column(db.Boolean)
    probation_status = db.Column(db.Boolean)

    
    def serialize(self):
        return {
            'criminal_id': self.criminal_id,
            'name': self.name,
            'violent_status': self.violent_status,
            'probation_status': self.probation_status
        }