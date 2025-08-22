from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from models.costumer import Costumer, costumers_schema, costumer_schema
from init import db
from psycopg2 import errorcodes

costumer_bp = Blueprint("costumer", __name__,url_prefix="/costumers")

# GET ALL COSTUMERS 
@costumer_bp.route("/")
def get_costumers():
    stmt = db.select(Costumer)
    costumers_list = db.session.scalars(stmt)
    data = costumers_schema.dump(costumers_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No costumers found."}, 404
    


# GET COSTUMER BY ID
@costumer_bp.route("/<int:costumer_id>")
def get_a_costumer(costumer_id):
    stmt = db.select(Costumer).where(Costumer.id == costumer_id)
    costumer = db.session.scalar(stmt)
    if costumer:
        data = costumer_schema.dump(costumer)
        return jsonify(data)
    else:
        return {"message":f"Costumer {costumer_id} does not exist."}, 404
    


# POST: CREATE A COSTUMER
@costumer_bp.route("/",methods = ["POST"])
def create_a_costumer():
    try:
        body_data = request.get_json()
        new_costumer = Costumer(
            name = body_data.get("name"),
            email = body_data.get("email"),
            contact = body_data.get("contact")
        )
        db.session.add(new_costumer)
        db.session.commit()

        return jsonify(costumer_schema.dump(new_costumer)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message":"Email has to be unique."}, 400
        else:
            return {"message":"Unexpected error has ocurred."}, 400
        


# DELETE: id
@costumer_bp.route("/<int:costumer_id>", methods=["DELETE"])
def delete_costumer(costumer_id):
    stmt = db.select(Costumer).where(Costumer.id == costumer_id)
    costumer = db.session.scalar(stmt)
    if costumer:
        db.session.delete(costumer)
        db.session.commit()
        return {"message": f"Costumer '{costumer.name}' has been removed succesfully."}, 200
    else:
        return{"message":f"Costumer does not exist."}, 404 
    


# UPDATE: /costumers/id
@costumer_bp.route("/<int:costumer_id>", methods=["PUT","PATCH"])
def update_costumer(costumer_id):
    stmt = db.select(Costumer).where(Costumer.id == costumer_id)
    costumer = db.session.scalar(stmt)
    if costumer:
        body_data = request.get_json()
        costumer.name = body_data.get("name") or costumer.name
        costumer.email = body_data.get("email") or costumer.email
        costumer.contact = body_data.get("contact") or costumer.contact
        db.session.commit()
        return jsonify(costumer_schema.dump(costumer))
    else:
        return {"message":f"Costumer with id {costumer_id} does not exist."}, 404