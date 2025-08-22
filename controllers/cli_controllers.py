from flask import Blueprint
from init import db
from models.order import Order
from models.costumer import Costumer
from models.artist import Artist
from models.writer import Writer
from models.publisher import Publisher
from models.comic import Comic

database_controller = Blueprint("db", __name__)


@database_controller.cli.command("create")
def create_table():
    db.create_all()
    print("Tables created.")


@database_controller.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Tables dropped.")


@database_controller.cli.command("seed")
def seed_table():
    
    costumers = [
        Costumer(name="Abby",
                 email="abby@email.com",
                 contact="0123456891",),
        
        Costumer(name="Agus",
                 email="agus@email.com",
                 contact="9876543210"),
        
        Costumer(name="Gaby",
                 email="gaby@email.com",
                 contact="0448135984")
    ]
    db.session.add_all(costumers)
    db.session.commit()



    orders = [
        Order(costumer_id=costumers[0].id,
              description="Paid. pick up next monday"),
        
        Order(costumer_id=costumers[1].id,
              description="Not paid, will pay when pick up.")
    ]
    db.session.add_all(orders)



    artists = [
        Artist(name="Dave Gibbons"),
        
        Artist(name="Frank Quitely"),
        
        Artist(name="Steve McNiven")
    ]
    db.session.add_all(artists)

   

    writers = [
        Writer(name="Alan Moore"),
        
        Writer(name="Grant Morrison"),
        
        Writer(name="Mark Millar")
    ]
    db.session.add_all(writers)



    publishers = [
        Publisher(name="DC Comics"),
        
        Publisher(name="Marvel Comics")
    ]
    db.session.add_all(publishers)
    db.session.commit()


    comics = [
        Comic(title="Watchmen",
              price="40",
              publisher_id=publishers[0].id,),
        
        Comic(title="Superman All Star",
              price="25",
              publisher_id=publishers[0].id,),
        
        Comic(title="Civil War",
              price="37",
              publisher_id=publishers[1].id,),
    ]
    db.session.add_all(comics)

    
    db.session.commit()

    print("Tables seeded.")
