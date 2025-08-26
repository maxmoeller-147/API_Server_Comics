from init import db

# Order Model
class Order(db.Model):
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(500), nullable=False)
    
	# Relationship with Costumer
	costumer_id = db.Column(db.Integer, db.ForeignKey("costumer.id"))
	costumer = db.relationship("Costumer", back_populates="orders")
	
	# relationship many to many with order_comics
	order_comics = db.relationship("OrderComic", back_populates="order", cascade="all, delete-orphan")



