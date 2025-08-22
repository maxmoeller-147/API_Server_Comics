from init import db


class Order(db.Model):
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(200), nullable=True)
    # Relationship with Costumer
	costumer_id = db.Column(db.Integer, db.ForeignKey("costumers.id"))
	costumer = db.relationship("Costumer", back_populates="orders")
	



