from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from models.writer import Writer
from models.artist import Artist
from models.comic import Comic
from schemas.schemas import comics_schema, comic_schema
from init import db


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
    



# POST: CREATE A COMIC
@comic_bp.route("/",methods = ["POST"])
def create_a_comic():
    body_data = request.get_json()
    if not body_data:
        return{"message":"Request Body must be included"}, 400
        


    # Validate Price    
    price_input = body_data.get("price")
    try:
        price_input = int(price_input)
    except (TypeError,ValueError):
            return {"message":"Price must be an integer."}, 400
    

    # Create Comic
    new_comic = Comic(title = body_data.get("title"), price = price_input, publisher_id = body_data.get("publisher_id"))

    

    # If Writer is provided 
    writer_ids = body_data.get("writer_ids", [])
    for writer_id in writer_ids:
        writer = db.session.get(Writer,writer_id)
        if writer:
            new_comic.writers.append(writer)



    # If Artist is provided 
    artist_ids = body_data.get("artist_ids", [])
    for artist_id in artist_ids:
        artist = db.session.get(Artist,artist_id)
        if artist:
            new_comic.artists.append(artist)



    # Error Handle
    try:
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
        
        






# UPDATE: /comics/id
@comic_bp.route("/<int:comic_id>", methods=["PUT","PATCH"])

def update_comic(comic_id):
    
    stmt = db.select(Comic).where(Comic.id == comic_id)
    comic = db.session.scalar(stmt)
    
    if comic:

        body_data = request.get_json()
        if not body_data:
            return {"message":"Request body must be included"}, 400    

       
        # Price Validation
        price_input = body_data.get("price")
        if price_input is not None:
            try:
                comic.price = int(price_input)
            except (TypeError, ValueError):
                return {"message": "Price must be an integer."}, 400
        
       
        # Update Publisher
        comic.publisher_id = body_data.get("publisher_id") or comic.publisher_id
        
       
        # Update Title
        comic.title = body_data.get("title") or comic.title
        
             
        # Update Writer
        writer_ids = body_data.get("writer_ids")
        if writer_ids is not None:
            comic.writers.clear()  
            for writer_id in writer_ids:
                writer = db.session.get(Writer, writer_id)
                if writer:
                    comic.writers.append(writer)



        # Update Artist
        artist_ids = body_data.get("artist_ids")
        if artist_ids is not None:
            comic.artists.clear()  
            for artist_id in artist_ids:
                artist = db.session.get(Artist, artist_id)
                if artist:
                    comic.artists.append(artist)


        db.session.commit()
        return jsonify(comic_schema.dump(comic))
    else:
        return {"message":f"Comic with id {comic_id} does not exist."}, 404
    