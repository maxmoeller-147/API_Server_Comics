from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import ValidationError

from init import db
from models.order import Order
from schemas.schemas import order_schema, orders_schema

order_bp = Blueprint("order",__name__, url_prefix="/orders")


# GET ALL ORDERS 
@order_bp.route("/")
def get_orders():
    id = request.args.get("id")
    if id:
        stmt = db.select(Order).where(Order.id == id)
    else:
        stmt = db.select(Order)  
    
    orders_list = db.session.scalars(stmt)
    data = orders_schema.dump(orders_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No orders found."}, 404
    



# GET ORDER BY ID
@order_bp.route("/<int:order_id>")
def get_a_order(order_id):
    stmt = db.select(Order).where(Order.id == order_id)
    order = db.session.scalar(stmt)
    if order:
        data = order_schema.dump(order)
        return jsonify(data)
    else:
        return {"message":f"Order {order_id} does not exist."}, 404
    



# DELETE: id
@order_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    stmt = db.select(Order).where(Order.id == order_id)
    order = db.session.scalar(stmt)
    
    if order:
        db.session.delete(order)
        db.session.commit()
        return {"message": f"Order '{order.id}' has been removed succesfully."}, 200
    else:
        return{"message":f"Order does not exist."}, 404 
    


    
# POST: CREATE A ORDER
@order_bp.route("/",methods = ["POST"])
def create_a_order():
  
    body_data = request.get_json()
    new_order = order_schema.load(body_data, session = db.session)
    db.session.add(new_order)
    db.session.commit()
    return jsonify(order_schema.dump(new_order)), 201
    



# UPDATE: /orders/id
@order_bp.route("/<int:order_id>", methods=["PUT","PATCH"])
def update_order(order_id):
    stmt = db.select(Order).where(Order.id == order_id)
    order = db.session.scalar(stmt)
    
    if not order:
        return {"message":f"Order with id {order_id} does not exist."}, 404
    
    else:
        body_data = request.get_json()
        order = order_schema.load(body_data,instance = order, session = db.session, partial= True)
        db.session.commit()
        return jsonify(order_schema.dump(order))
    

       
