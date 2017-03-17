from application import db

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64), index=True)
    lastName = db.Column(db.String(64), index=True)
    dob = db.Column(db.String(120), index=True)
    dod = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<id {}, lastName {}>'.format(self.uid, self.lastName)
