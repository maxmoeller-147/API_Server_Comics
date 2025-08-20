from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Costumer Model
class Costumer(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(20))


class CostumerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Costumer
        load_instance = True

# Schema for single entry
costumer_schema = CostumerSchema()

# Schema for multiple entries
costumers_schema = CostumerSchema(many=True)