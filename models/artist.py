from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Artist Model
class Artist(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        load_instance = True

# Schema for single entry
artist_schema = ArtistSchema()

# Schema for multiple entries
artists_schema = ArtistSchema(many=True) 