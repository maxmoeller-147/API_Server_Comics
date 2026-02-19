from main import create_app
from init import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database schema created")
