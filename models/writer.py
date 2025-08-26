from init import db
from models.comic_writer import comic_writer

# Writer Model
class Writer(db.Model):
    __tablename__ = "writers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

   # Relationship with Comic (many to many)
    comics = db.relationship("Comic", secondary=comic_writer, back_populates="writers")