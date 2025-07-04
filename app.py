from flask import Flask, render_template, request, redirect, url_for
from models import db, Flight, Bookmark
from data_utils import get_mock_data, analyze_data, save_data_to_db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not Flight.query.first():
        mock_data = get_mock_data()
        save_data_to_db(mock_data)

@app.route("/")
def dashboard():
    origin = request.args.get('from')
    destination = request.args.get('to')
    flights = Flight.query.all()
    insights = analyze_data(flights, origin, destination)
    return render_template("dashboard.html", insights=insights, origin=origin, destination=destination)

@app.route("/bookmark/<int:flight_id>")
def bookmark(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    bookmark = Bookmark(route=flight.route, date=flight.date, price=flight.price)
    db.session.add(bookmark)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/admin")
def admin():
    bookmarks = Bookmark.query.all()
    return render_template("admin.html", bookmarks=bookmarks)

if __name__ == "__main__":
    app.run(debug=True)
