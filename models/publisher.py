from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Publisher Model
class Publisher(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class PublisherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher
        load_instance = True

# Schema for single entry
publisher_schema = PublisherSchema()

# Schema for multiple entries
publishers_schema = PublisherSchema(many=True) 