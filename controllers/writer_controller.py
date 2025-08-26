from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import ValidationError

from models.writer import Writer
from schemas.schemas import writers_schema, writer_schema
from init import db


writer_bp = Blueprint("writer", __name__,url_prefix="/writers")


# GET ALL WRITERS 
@writer_bp.route("/")
def get_writers():
    name = request.args.get("name")
    if name:
        stmt = db.select(Writer).where(Writer.name == name)
    else:
        stmt = db.select(Writer)

    writers_list = db.session.scalars(stmt)
    data = writers_schema.dump(writers_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No writer found."}, 404




# GET WRITERS BY ID
@writer_bp.route("/<int:writer_id>")
def get_a_writer(writer_id):
    stmt = db.select(Writer).where(Writer.id == writer_id)
    writer = db.session.scalar(stmt)
    if writer:
        data = writer_schema.dump(writer)
        return jsonify(data)
    else:
        return {"message":f"Writer {writer_id} does not exist."}, 404
    



# DELETE: id
@writer_bp.route("/<int:writer_id>", methods=["DELETE"])
def delete_writer(writer_id):
    stmt = db.select(Writer).where(Writer.id == writer_id)
    writer = db.session.scalar(stmt)
    if writer:
        db.session.delete(writer)
        db.session.commit()
        return {"message": f"Writer '{writer.name}' has been removed succesfully."}, 200
    else:
        return{"message":f"Writer does not exist."}, 404
    



# CREATE A WRITER
@writer_bp.route("/",methods = ["POST"])
def create_a_writer():
    
    body_data = request.get_json()
    new_writer = writer_schema.load(body_data, session = db.session)
    db.session.add(new_writer)
    db.session.commit()
    return jsonify(writer_schema.dump(new_writer)), 201
            



 # UPDATE: /writers/id
@writer_bp.route("/<int:writer_id>", methods=["PUT","PATCH"])
def update_writer(writer_id):
    stmt = db.select(Writer).where(Writer.id == writer_id)
    writer = db.session.scalar(stmt)
    
    if not writer:
         return {"message":f"Writer with id {writer_id} does not exist."}, 404
        
    else:
        body_data = request.get_json()
        writer = writer_schema.load(body_data,instance = writer, session = db.session, partial= True)
        db.session.commit()
        return jsonify(writer_schema.dump(writer))
    

  
