from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from marshmallow.validate import Length, Email, Regexp
  

from models.costumer import Costumer
from models.order import Order
from models.artist import Artist
from models.writer import Writer
from models.publisher import Publisher
from models.comic import Comic
from models.order_comic import OrderComic


# Costumer Schema:
class CostumerSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    orders = fields.List(fields.Nested("OrderSchema", exclude=("costumer",)))
    class Meta:
        model = Costumer
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id","name","email","contact","orders")
        ordered = True


    name = auto_field(validate=[
     Length(min=2, error="Costumer Name is too short.")])
    
    email = auto_field(validate=[
     Email(error="Costumer Email is invalid.")])
    
    contact = auto_field(validate=[
        Length(equal=10, error="Phone number must be 10 values."),
        Regexp(r'^\d{10}$', error=" Please use only numbers")
     ])



# Order Schema:
class OrderSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    order_comics = fields.List(fields.Nested("OrderComicSchema", exclude=("order",)))
    costumer = fields.Nested("CostumerSchema", exclude=("orders","id",))
    costumer_id = auto_field(required=True)
    class Meta:
        model = Order
        load_instance = True 
        include_fk = True
        include_relationships = True
        fields = ("id","costumer_id","costumer","order_comics","description") 
        ordered = True   
        


# Artist Schema:
class ArtistSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    comics = fields.List(fields.Nested(lambda: ComicSchema(exclude=("artists","id",))))
    class Meta:
        model = Artist
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True

    name = auto_field(validate=[
      Length(min=2, error="Artist Name is too short.")])



# Writer Schema:
class WriterSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    comics = fields.List(fields.Nested(lambda: ComicSchema(exclude=("writers","id",))))
    class Meta:
        model = Writer
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True

    name = auto_field(validate=[
     Length(min=2, error="Writer Name is too short.")])



# Publisher Schema:
class PublisherSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    comics = fields.List(fields.Nested("ComicSchema", exclude=("publisher","id",))) 
    class Meta:   
        model = Publisher
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("name","id","comics")
        ordered = True

    name = auto_field(validate=[
     Length(min=2, error="Publisher Name is too short.")])


# Comic Schema:
class ComicSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    order_comics = fields.List(fields.Nested("OrderComicSchema", exclude=("comic",)))
    writers = fields.List(fields.Nested(lambda: WriterSchema(exclude=("comics",))))
    artists = fields.List(fields.Nested(lambda: ArtistSchema(exclude=("comics",))))
    publisher = fields.Nested("PublisherSchema", exclude=("comics",))
    class Meta:
        model = Comic
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id","price", "title","publisher", "artists","writers","order_comics")
        ordered = True




# Order_Comic Schema:
class OrderComicSchema(SQLAlchemyAutoSchema):
    id = auto_field(load_only=True)
    comic = fields.Nested("ComicSchema", exclude=("order_comics",))
    order = fields.Nested("OrderSchema", exclude=("order_comics",))
    class Meta:
        model = OrderComic
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id","order_id","comic_id","quantity", "order", "comic")
        ordered=True



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

order_comic_schema = OrderComicSchema()
order_comics_schema = OrderComicSchema(many=True)


