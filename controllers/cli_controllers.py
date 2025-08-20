from flask import Blueprint
from init import db
from models.costumer import Costumer

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
    print("Tables seeded.")
