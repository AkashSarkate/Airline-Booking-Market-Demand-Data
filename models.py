from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(20))
    price = db.Column(db.Float)
    date = db.Column(db.String(10))

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(20))
    price = db.Column(db.Float)
    date = db.Column(db.String(10))
