from init import db
from models.comic_artist import comic_artist
from models.comic_writer import comic_writer

class Comic(db.Model):
	__tablename__ = "comics"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False, unique=True) 
	price = db.Column(db.Integer, nullable=False)
    
	# Relationship with Publisher
	publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"))
	publisher = db.relationship("Publisher", back_populates="comics")

	# Relationship with Artist (many to many)
	artists = db.relationship("Artist", secondary=comic_artist, back_populates="comics")

	# Relationship with Writer (many to many)
	writers = db.relationship("Writer", secondary=comic_writer, back_populates="comics")