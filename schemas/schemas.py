from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.costumer import Costumer
from models.order import Order
from models.artist import Artist
from models.writer import Writer
from models.publisher import Publisher
from models.comic import Comic


# Costumer Schema:
class CostumerSchema(SQLAlchemyAutoSchema):
    orders = fields.List(fields.Nested("OrderSchema", exclude=("costumer",)))
    class Meta:
        model = Costumer
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id","name","email","contact","orders")
        ordered = True



# Order Schema:
class OrderSchema(SQLAlchemyAutoSchema):
    costumer = fields.Nested("CostumerSchema", exclude=("orders",))
    class Meta:
        model = Order
        load_instance = True 
        include_fk = True
        include_relationships = True
        fields = ("id","costumer","description") 
        ordered = True   



# Artist Schema:
class ArtistSchema(SQLAlchemyAutoSchema):
    comics = fields.List(fields.Nested(lambda: ComicSchema(exclude=("artists",))))
    class Meta:
        model = Artist
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True


# Writer Schema:
class WriterSchema(SQLAlchemyAutoSchema):
    comics = fields.List(fields.Nested(lambda: ComicSchema(exclude=("writers",))))
    class Meta:
        model = Writer
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True



# Publisher Schema:
class PublisherSchema(SQLAlchemyAutoSchema):
    comics = fields.List(fields.Nested("ComicSchema", exclude=("publisher",))) 
    class Meta:   
        model = Publisher
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True



# Comic Schema:
class ComicSchema(SQLAlchemyAutoSchema):
    writers = fields.List(fields.Nested(lambda: WriterSchema(exclude=("comics",))))
    artists = fields.List(fields.Nested(lambda: ArtistSchema(exclude=("comics",))))
    publisher = fields.Nested("PublisherSchema", exclude=("comics",))
    class Meta:
        model = Comic
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id","price", "title","publisher", "artists","writers")
        ordered = True




# Schemas for single and multiple entries
costumer_schema = CostumerSchema()
costumers_schema = CostumerSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True) 

writer_schema = WriterSchema()
writers_schema = WriterSchema(many=True) 

publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True) 

comic_schema = ComicSchema()
comics_schema = ComicSchema(many=True)

