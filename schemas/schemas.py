from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.costumer import Costumer
from models.order import Order
from models.artist import Artist
from models.writer import Writer
from models.publisher import Publisher


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

# Artist Schema:
class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        load_instance = True

# Writer Schema:
class WriterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Writer
        load_instance = True

# Publisher Schema:
class PublisherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher
        load_instance = True




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

