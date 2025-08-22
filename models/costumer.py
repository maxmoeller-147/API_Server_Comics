from init import db

# Costumer Model
class Costumer(db.Model):
    __tablename__="costumer"
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(20))
    # Relationship with Orders
    orders = db.relationship("Order", back_populates="costumer", cascade="all, delete-orphan")


