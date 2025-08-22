from init import db


# Writer Model
class Writer(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


