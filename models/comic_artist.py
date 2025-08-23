from init import db


# Join Table (Not Model as it doesn't include any extra fields)
comic_artist = db.Table (
    "comic_artist",
    db.Column("comic_id",db.Integer,db.ForeignKey("comics.id"), primary_key=True),
    db.Column("artist_id", db.Integer,db.ForeignKey("artists.id"), primary_key=True)
)

