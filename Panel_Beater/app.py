from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os 
from flask_wtf import CSRFProtect

app = Flask(__name__)
CORS(app)  # Allow requests from frontend
csrf = CSRFProtect(app)


# Used SQLite for testing 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///panelB_booking.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_make = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    preferred_date = db.Column(db.String(20))
    description = db.Column(db.Text)

# Created the database and tables 
with app.app_context():
    db.create_all()

# Define the routes
@app.route('/')
def index():
    return render_template('panel.html')    

# Route to handle booking submissions
@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json

    try:
        booking = Booking(
            customer_name=data['customerName'],
            email=data['email'],
            phone=data['phone'],
            vehicle_make=data['vehicleMake'],
            service_type=data['serviceType'],
            preferred_date=data.get('preferredDate', ''),
            description=data.get('description', '')
        )

        db.session.add(booking)
        db.session.commit()

        return jsonify({'message': 'Booking saved successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
