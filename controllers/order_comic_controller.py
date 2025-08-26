from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from models.order_comic import OrderComic
from schemas.schemas import order_comics_schema, order_comic_schema
from init import db


order_comic_bp = Blueprint("order_comic", __name__,url_prefix="/order_comics")



# GET ALL ORDER_COMICS 
@order_comic_bp.route("/")
def get_order_comics():
    stmt = db.select(OrderComic)
    order_comics_list = db.session.scalars(stmt)
    data = order_comics_schema.dump(order_comics_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No order_comic found."}, 404
    


# GET ORDER_COMIC BY ID
@order_comic_bp.route("/<int:order_comic_id>")
def get_order_comic(order_comic_id):
    stmt = db.select(OrderComic).where(OrderComic.id == order_comic_id)
    order_comic = db.session.scalar(stmt)
    if order_comic:
        data = order_comic_schema.dump(order_comic) 
        return jsonify(data)
    return {"message": f"OrderComic with order_comic_id={order_comic_id} not found."}, 404




# DELETE: id
@order_comic_bp.route("/<int:order_comic_id>", methods=["DELETE"])
def delete_order_comic(order_comic_id):
    stmt = db.select(OrderComic).where(OrderComic.id == order_comic_id)
    order_comic = db.session.scalar(stmt)
    if order_comic:
        db.session.delete(order_comic)
        db.session.commit()
        return {"message": f"Order_comic '{order_comic_id}' has been removed succesfully."}, 200
    else:
        return{"message":f"Order_comic does not exist."}, 404
    


# CREATE AN ORDER_COMIC
@order_comic_bp.route("/",methods = ["POST"])
def create_an_order_comic():  
    
    body_data = request.get_json()
    new_order_comic = order_comic_schema.load(body_data, session = db.session)
    db.session.add(new_order_comic)
    db.session.commit()
    return jsonify(order_comic_schema.dump(new_order_comic)), 201
    
 


# UPDATE: /order_comics/id
@order_comic_bp.route("/<int:order_comic_id>", methods=["PUT","PATCH"])
def update_order_comic(order_comic_id):
    stmt = db.select(OrderComic).where(OrderComic.id == order_comic_id)
    order_comic = db.session.scalar(stmt)
   
    if not order_comic:
        return {"message":f"Order_comic with id {order_comic_id} does not exist."}, 404   
        
    else:
        body_data = request.get_json()
        order_comic = order_comic_schema.load(body_data,instance= order_comic, session = db.session, partial = True)
        db.session.commit()
        return jsonify(order_comic_schema.dump(order_comic))
   