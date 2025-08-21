from flask import Blueprint, jsonify, request 
from models.costumer import Costumer, costumers_schema, costumer_schema
from init import db

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
    

# CREATE A COSTUMER
@costumer_bp.route("/",methods = ["POST"])
def create_a_costumer():
    body_data = request.get_json()
    new_costumer = Costumer(
        name = body_data.get("name"),
        email = body_data.get("email"),
        contact = body_data.get("contact")
    )
    db.session.add(new_costumer)
    db.session.commit()

    return jsonify(costumer_schema.dump(new_costumer)), 201