from init import db


# Artist Model
class Artist(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


