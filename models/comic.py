from init import db


class Comic(db.Model):
	__tablename__ = "comics"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False, unique=True) 
	price = db.Column(db.Integer, nullable=False)
    # Relationship with Publisher
	publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"))
	publisher = db.relationship("Publisher", back_populates="comics")