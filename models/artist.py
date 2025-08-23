from init import db
from models.comic_artist import comic_artist

# Artist Model
class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship with Comic (many to many)
    comics = db.relationship("Comic", secondary=comic_artist, back_populates="artists")