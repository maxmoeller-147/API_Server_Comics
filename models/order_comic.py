from init import db

# OrderComic Model
class OrderComic(db.Model):
    __tablename__ = "order_comics"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey("comics.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False,default=1)

    # Relationship with Order
    order = db.relationship("Order", back_populates="order_comics")
    # Relationship with Comic
    comic = db.relationship("Comic", back_populates="order_comics")