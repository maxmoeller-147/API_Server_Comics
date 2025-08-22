from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from models.comic import Comic
from schemas.schemas import comics_schema, comic_schema
from init import db
from psycopg2 import errorcodes

comic_bp = Blueprint("comic", __name__,url_prefix="/comics")

# GET ALL COMICS 
@comic_bp.route("/")
def get_comics():
    stmt = db.select(Comic)  
    comics_list = db.session.scalars(stmt)
    data = comics_schema.dump(comics_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No comics found."}, 404
    


# GET COMIC BY ID
@comic_bp.route("/<int:comic_id>")
def get_a_comic(comic_id):
    stmt = db.select(Comic).where(Comic.id == comic_id)
    comic = db.session.scalar(stmt)
    if comic:
        data = comic_schema.dump(comic)
        return jsonify(data)
    else:
        return {"message":f"Comic {comic_id} does not exist."}, 404
    


# POST: CREATE A COMIC
@comic_bp.route("/",methods = ["POST"])
def create_a_comic():
    try:
        body_data = request.get_json()
        new_comic = Comic(
            publisher_id = body_data.get("publisher_id"),
            title = body_data.get("title"),
            price = body_data.get("price")
        )
        db.session.add(new_comic)
        db.session.commit()

        return jsonify(comic_schema.dump(new_comic)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message":"Title has to be unique."}, 400
        else:
            return {"message":"Unexpected error has ocurred."}, 400
        
        ### NEED TO VALIDATE TO AVOID THE InVALID Interger Error
        


# DELETE: id
@comic_bp.route("/<int:comic_id>", methods=["DELETE"])
def delete_comic(comic_id):
    stmt = db.select(Comic).where(Comic.id == comic_id)
    comic = db.session.scalar(stmt)
    if comic:
        db.session.delete(comic)
        db.session.commit()
        return {"message": f"Comic '{comic.title}' has been removed succesfully."}, 200
    else:
        return{"message":f"Comic does not exist."}, 404 
    


# UPDATE: /comics/id
@comic_bp.route("/<int:comic_id>", methods=["PUT","PATCH"])
def update_comic(comic_id):
    stmt = db.select(Comic).where(Comic.id == comic_id)
    comic = db.session.scalar(stmt)
    if comic:
        body_data = request.get_json()
        comic.publisher_id = body_data.get("publisher_id") or comic.publisher_id
        comic.title = body_data.get("title") or comic.title
        comic.price = body_data.get("price") or comic.price
        db.session.commit()
        return jsonify(comic_schema.dump(comic))
    else:
        return {"message":f"Comic with id {comic_id} does not exist."}, 404
    
      ### NEED TO VALIDATE TO AVOID THE InVALID Interger Error