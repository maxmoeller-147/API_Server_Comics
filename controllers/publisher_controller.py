from flask import Blueprint, jsonify, request 
from models.publisher import Publisher
from schemas.schemas import publishers_schema, publisher_schema
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

publisher_bp = Blueprint("publisher", __name__,url_prefix="/publishers")

# GET ALL PUBLISHERS 
@publisher_bp.route("/")
def get_publishers():
    stmt = db.select(Publisher)
    publishers_list = db.session.scalars(stmt)
    data = publishers_schema.dump(publishers_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No publisher found."}, 404
    


# GET PUBLISHERS BY ID
@publisher_bp.route("/<int:publisher_id>")
def get_a_publisher(publisher_id):
    stmt = db.select(Publisher).where(Publisher.id == publisher_id)
    publisher = db.session.scalar(stmt)
    if publisher:
        data = publisher_schema.dump(publisher)
        return jsonify(data)
    else:
        return {"message":f"Publisher {publisher_id} does not exist."}, 404
    


# CREATE A PUBLISHER
@publisher_bp.route("/",methods = ["POST"])
def create_a_publisher():
    try:
        body_data = request.get_json()
        new_publisher = Publisher(name = body_data.get("name"))
        db.session.add(new_publisher)
        db.session.commit()

        return jsonify(publisher_schema.dump(new_publisher)), 201
            
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message":"Name has to be unique."}, 400
        else:
            return {"message":"Unexpected error has ocurred."}, 400



# DELETE: id
@publisher_bp.route("/<int:publisher_id>", methods=["DELETE"])
def delete_publisher(publisher_id):
    stmt = db.select(Publisher).where(Publisher.id == publisher_id)
    publisher = db.session.scalar(stmt)
    if publisher:
        db.session.delete(publisher)
        db.session.commit()
        return {"message": f"Publisher '{publisher.name}' has been removed succesfully."}, 200
    else:
        return{"message":f"Publisher does not exist."}, 404
    


 # UPDATE: /publishers/id
@publisher_bp.route("/<int:publisher_id>", methods=["PUT","PATCH"])
def update_publisher(publisher_id):
    stmt = db.select(Publisher).where(Publisher.id == publisher_id)
    publisher = db.session.scalar(stmt)
    if publisher:
        body_data = request.get_json()
        publisher.name = body_data.get("name") or publisher.name
        db.session.commit()
        return jsonify(publisher_schema.dump(publisher))
    else:
        return {"message":f"Publisher with id {publisher_id} does not exist."}, 404
