from init import db


# Publisher Model
class Publisher(db.Model):
    __tablename__ = "publisher"
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Relationship with comics
    comics = db.relationship("Comic", back_populates="publisher")


