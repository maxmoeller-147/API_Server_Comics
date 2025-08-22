from flask import Blueprint, jsonify, request 
from models.artist import Artist
from schemas.schemas import artists_schema, artist_schema
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

artist_bp = Blueprint("artist", __name__,url_prefix="/artists")

# GET ALL ARTISTS 
@artist_bp.route("/")
def get_artists():
    stmt = db.select(Artist)
    artists_list = db.session.scalars(stmt)
    data = artists_schema.dump(artists_list)
    
    if data:
        return jsonify(data)
    elif data == []:
        return {"message":"No artist found."}, 404
    


# GET ARTIST BY ID
@artist_bp.route("/<int:artist_id>")
def get_an_artist(artist_id):
    stmt = db.select(Artist).where(Artist.id == artist_id)
    artist = db.session.scalar(stmt)
    if artist:
        data = artist_schema.dump(artist)
        return jsonify(data)
    else:
        return {"message":f"Artist {artist_id} does not exist."}, 404
    


# CREATE AN ARTIST
@artist_bp.route("/",methods = ["POST"])
def create_an_artist():
    try:
        body_data = request.get_json()
        new_artist = Artist(name = body_data.get("name"))
        db.session.add(new_artist)
        db.session.commit()

        return jsonify(artist_schema.dump(new_artist)), 201
            
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message":"Name has to be unique."}, 400
        else:
            return {"message":"Unexpected error has ocurred."}, 400



# DELETE: id
@artist_bp.route("/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    stmt = db.select(Artist).where(Artist.id == artist_id)
    artist = db.session.scalar(stmt)
    if artist:
        db.session.delete(artist)
        db.session.commit()
        return {"message": f"Artist '{artist.name}' has been removed succesfully."}, 200
    else:
        return{"message":f"Artist does not exist."}, 404
    


 # UPDATE: /artists/id
@artist_bp.route("/<int:artist_id>", methods=["PUT","PATCH"])
def update_artist(artist_id):
    stmt = db.select(Artist).where(Artist.id == artist_id)
    artist = db.session.scalar(stmt)
    if artist:
        body_data = request.get_json()
        artist.name = body_data.get("name") or artist.name
        db.session.commit()
        return jsonify(artist_schema.dump(artist))
    else:
        return {"message":f"Artist with id {artist_id} does not exist."}, 404
