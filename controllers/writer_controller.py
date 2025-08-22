from flask import Blueprint, jsonify, request 
from models.writer import Writer, writers_schema, writer_schema
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

writer_bp = Blueprint("writer", __name__,url_prefix="/writers")

# GET ALL WRITERS 
@writer_bp.route("/")
def get_writers():
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
    


# CREATE A WRITER
@writer_bp.route("/",methods = ["POST"])
def create_a_writer():
    try:
        body_data = request.get_json()
        new_writer = Writer(name = body_data.get("name"))
        db.session.add(new_writer)
        db.session.commit()

        return jsonify(writer_schema.dump(new_writer)), 201
            
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message":"Name has to be unique."}, 400
        else:
            return {"message":"Unexpected error has ocurred."}, 400



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
    


 # UPDATE: /writers/id
@writer_bp.route("/<int:writer_id>", methods=["PUT","PATCH"])
def update_writer(writer_id):
    stmt = db.select(Writer).where(Writer.id == writer_id)
    writer = db.session.scalar(stmt)
    if writer:
        body_data = request.get_json()
        writer.name = body_data.get("name") or writer.name
        db.session.commit()
        return jsonify(writer_schema.dump(writer))
    else:
        return {"message":f"Writer with id {writer_id} does not exist."}, 404
