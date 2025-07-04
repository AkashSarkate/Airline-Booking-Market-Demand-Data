import plotly.express as px
import pandas as pd
from models import db, Flight

def get_mock_data():
    return [
        {"route": "SYD-MEL", "price": 150, "date": "2025-07-04"},
        {"route": "SYD-MEL", "price": 155, "date": "2025-07-04"},
        {"route": "SYD-BNE", "price": 200, "date": "2025-07-05"},
        {"route": "SYD-MEL", "price": 145, "date": "2025-07-06"},
        {"route": "MEL-SYD", "price": 140, "date": "2025-07-06"},
        {"route": "BNE-MEL", "price": 170, "date": "2025-07-07"},
    ]

def save_data_to_db(data):
    for item in data:
        flight = Flight(route=item["route"], price=item["price"], date=item["date"])
        db.session.add(flight)
    db.session.commit()

def analyze_data(flights, origin=None, destination=None):
    df = pd.DataFrame([{"route": f.route, "price": f.price, "date": f.date} for f in flights])
    if origin:
        df = df[df['route'].str.startswith(origin)]
    if destination:
        df = df[df['route'].str.endswith(destination)]

    chart_html = ""
    price_chart = ""

    if not df.empty:
        route_counts = df['route'].value_counts().reset_index()
        route_counts.columns = ['Route', 'Bookings']
        fig = px.bar(route_counts, x='Route', y='Bookings', title='Popular Routes')
        chart_html = fig.to_html(full_html=False)

        date_avg = df.groupby('date')['price'].mean().reset_index()
        fig2 = px.line(date_avg, x='date', y='price', title='Price Trend Over Time')
        price_chart = fig2.to_html(full_html=False)

    return {
        "popular_routes": df['route'].value_counts().to_dict(),
        "avg_price": df.groupby('route')['price'].mean().round(2).to_dict(),
        "high_demand_dates": df['date'].value_counts().head(5).to_dict(),
        "chart_html": chart_html,
        "price_chart": price_chart
    }
