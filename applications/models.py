from flask_login import UserMixin
from .database import db
from datetime import datetime

class User(db.Model,UserMixin):
    user_id = db.Column(db.String,primary_key = True,nullable = False, unique = True)
    password = db.Column(db.String,nullable=False)
    name = db.Column(db.String)
    email_id = db.Column(db.String)
    phone_no = db.Column(db.Integer)
    address = db.Column(db.String)
    bookings= db.relationship('Booking',backref='user')

    def get_id(self):
        return self.user_id

class Admin(db.Model,UserMixin):
    user_id = db.Column(db.String,primary_key = True,nullable = False, unique = True)
    password = db.Column(db.String,nullable=False)
    name = db.Column(db.String)
    email_id = db.Column(db.String)
    phone_no = db.Column(db.Integer)
    venues = db.relationship("Venue", backref='admin')
    shows = db.relationship("Show",backref='admin')

    def get_id(self):
        return self.user_id

class Venue(db.Model):
    venue_id = db.Column(db.Integer,primary_key = True, nullable = False,unique = True, autoincrement = True)
    venue_name = db.Column(db.String,nullable = False)
    location = db.Column(db.String,nullable = False)
    address = db.Column(db.String)
    capacity = db.Column(db.String)
    admin_id = db.Column(db.String,db.ForeignKey('admin.user_id'))
    venue_img_url = db.Column(db.String)
    shows = db.relationship("Show",backref='venues')
    
    # admin = db.relationship('Admin',back_polpulates='venues')

class Show(db.Model):
    show_id = db.Column(db.Integer,primary_key = True, nullable = False, unique = True, autoincrement = True)
    show_name = db.Column(db.String,nullable = False)
    description = db.Column(db.String,nullable = False)
    tags = db.Column(db.String)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.venue_id'),nullable=False)
    ticket_price = db.Column(db.Double,nullable = False)
    admin_id = db.Column(db.String,db.ForeignKey('admin.user_id'),nullable = False)
    timing = db.Column(db.DateTime, nullable = False)
    rating = db.Column(db.Double,nullable=False)
    rseats = db.Column(db.Integer)
    bookings = db.relationship('Booking',backref='show', cascade='all, delete')

class Booking(db.Model):
    booking_id = db.Column(db.Integer,primary_key = True, nullable=False,unique = True,autoincrement=True)
    user_id = db.Column(db.String,db.ForeignKey('user.user_id'),nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('show.show_id'),nullable=False)
    tickets_booked = db.Column(db.Integer,nullable=False)
    price_paid = db.Column(db.Double,nullable=False)

