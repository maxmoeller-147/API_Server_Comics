from flask import Blueprint, jsonify, request 
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import ValidationError

from models.artist import Artist
from schemas.schemas import artists_schema, artist_schema
from init import db


artist_bp = Blueprint("artist", __name__,url_prefix="/artists")


# GET ALL ARTISTS 
@artist_bp.route("/")
def get_artists():
    name = request.args.get("name")
    if name:
        stmt = db.select(Artist).where(Artist.name == name)
    else:
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
    



# CREATE AN ARTIST
@artist_bp.route("/",methods = ["POST"])
def create_an_artist():

    body_data = request.get_json()
    new_artist = artist_schema.load(body_data, session = db.session)
    db.session.add(new_artist)
    db.session.commit()
    return jsonify(artist_schema.dump(new_artist)), 201

    


# UPDATE: /artists/id
@artist_bp.route("/<int:artist_id>", methods=["PUT","PATCH"])
def update_artist(artist_id):
    stmt = db.select(Artist).where(Artist.id == artist_id)
    artist = db.session.scalar(stmt)
    
    if not artist:
        return {"message":f"Artist with id {artist_id} does not exist."}, 404
    
    else:
        body_data = request.get_json()
        artist = artist_schema.load(body_data,instance = artist, session = db.session, partial= True)
        db.session.commit()
        return jsonify(artist_schema.dump(artist))
    

        
