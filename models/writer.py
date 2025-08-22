from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Writer Model
class Writer(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class WriterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Writer
        load_instance = True

# Schema for single entry
writer_schema = WriterSchema()

# Schema for multiple entries
writers_schema = WriterSchema(many=True) 