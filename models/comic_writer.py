from init import db


# Join Table (Not Model as it doesn't include any extra fields)
comic_writer = db.Table (
    "comic_writer",
    db.Column("comic_id",db.Integer,db.ForeignKey("comics.id"), primary_key=True),
    db.Column("writer_id", db.Integer,db.ForeignKey("writers.id"), primary_key=True)
)

