from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)

# Create DB if it doesn't exist
with app.app_context():
    db.create_all()

# Read HTML template
with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

@app.route('/')
def home():
    return render_template_string(html_content)

@app.route('/services')
def services():
    return '''
    <h2>Our Beauty Services</h2>
    <ul>
        <li>💇‍♀️ Haircut - ₹300</li>
        <li>💆‍♀️ Facial - ₹500</li>
        <li>💅 Manicure - ₹400</li>
        <li>🦶 Pedicure - ₹450</li>
        <li>👰 Bridal Makeup - ₹2000</li>
    </ul>
    <a href='/'>Back to Booking</a>
    '''

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date = request.form.get('date')
    time = request.form.get('time')
    service = request.form.get('service')

    # Check for slot conflict
    existing = Booking.query.filter_by(date=date, time=time).first()
    if existing:
        return f'''
        <h2>Slot Unavailable</h2>
        <p>Sorry, the slot on {date} at {time} is already booked.</p>
        <a href='/'>Go Back</a>
        '''

    new_booking = Booking(
        name=name,
        email=email,
        phone=phone,
        date=date,
        time=time,
        service=service
    )

    db.session.add(new_booking)
    db.session.commit()

    return f'''
    <h2>Booking Confirmed!</h2>
    <p>Thank you, {name}. Your <strong>{service}</strong> appointment is confirmed for <strong>{date}</strong> at <strong>{time}</strong>.</p>
    <a href='/'>Book Another</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
