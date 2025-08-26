from flask import Blueprint, jsonify, request 
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from models.costumer import Costumer
from schemas.schemas import costumers_schema, costumer_schema
from init import db


costumer_bp = Blueprint("costumer", __name__,url_prefix="/costumers")


# GET ALL COSTUMERS 
@costumer_bp.route("/")
def get_costumers():
    name = request.args.get("name")
    if name:
        stmt = db.select(Costumer).where(Costumer.name == name)
    else:
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
    



# POST: CREATE A COSTUMER
@costumer_bp.route("/",methods = ["POST"])
def create_a_costumer():
 
    body_data = request.get_json()
    new_costumer = costumer_schema.load(body_data, session = db.session)
    db.session.add(new_costumer)
    db.session.commit()
    return jsonify(costumer_schema.dump(new_costumer)), 201
    

 

# UPDATE: /costumers/id
@costumer_bp.route("/<int:costumer_id>", methods=["PUT","PATCH"])
def update_costumer(costumer_id):
    stmt = db.select(Costumer).where(Costumer.id == costumer_id)
    costumer = db.session.scalar(stmt)
    
    if not costumer:
        return {"message":f"Costumer with id {costumer_id} does not exist."}, 404
    
    else:
        body_data = request.get_json()
        costumer = costumer_schema.load(body_data,instance = costumer, session = db.session, partial= True)
        db.session.commit()
        return jsonify(costumer_schema.dump(costumer))
    

   
       