from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from .models import *
from .validation import *

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('name')
update_user_parser.add_argument('email_id')
update_user_parser.add_argument('phone_no')
update_user_parser.add_argument('address')

resource_user = {
    'user_id': fields.String,
    'name': fields.String,
    'email_id': fields.String,
    'phone_no':fields.Integer,
    'address': fields.String
}

resource_booking={
    'booking_id':fields.Integer,
    'show_id': fields.Integer,
    'tickets_booked': fields.Integer,
    'price_paid': fields.Integer
}
bookings = fields.List(fields.Nested(resource_booking))

resource_venue={
    'venue_id': fields.Integer,
    'venue_name':fields.String,
    'location':fields.String,
    'address':fields.String,
    'capacity':fields.Integer,
    'venue_img_url':fields.String
}

resource_show={
    'show_id':fields.Integer,
    'show_name':fields.String,
    'description': fields.String,
    'timing':fields.String,
    'tags': fields.String,
    'venues': fields.List(fields.Nested(resource_venue)),
    'ticket_price': fields.Float,
    'rating':fields.Float
}

class UserProfile(Resource):
    @marshal_with(resource_user)
    def get(self,userID):
        user = User.query.filter_by(user_id = userID).first()
        if user is None:
            raise NotFoundError(status_code=404)
        return user
    
    @marshal_with(resource_user)
    def put(self,userID):
        args = update_user_parser.parse_args()
        name = args.get('name',None)
        phone_no = args.get('phone_no',None)
        address=args.get('address',None)
        email_id = args.get('email_id',None)
        print(name)
        if name is None:
            raise BusinessValidationError(status_code=400,error_code='BL101',error_message='Invalid Name')
        if phone_no is None or len(str(phone_no)) != 10:
            raise BusinessValidationError(status_code=400,error_code='BL102',error_message='Invalid Mobile Number')
        if '@'  not in email_id:
            raise BusinessValidationError(status_code=400,error_code='BL103',error_message='Invalid Email Id')
        
        if User.query.filter_by(user_id = userID).first() is None:
            raise NotFoundError(status_code=404)
        
        User.query.filter_by(user_id=userID).update({'name':name,
                                                     'phone_no':phone_no,
                                                     'email_id':email_id,
                                                     'address': address})
        db.session.commit()
        user = User.query.filter_by(user_id=userID).first()
        return user
    
    def delete(self,userID):
        user = User.query.filter_by(user_id = userID).first()
        if user is None:
            raise NotFoundError(status_code=404)
        db.session.delete(user)
        db.session.commit()
        return make_response('',200)
    
class UserBooking(Resource):
    @marshal_with(resource_booking)
    def get(self,userID):
        if User.query.filter_by(user_id = userID).first() is None:
            raise NotFoundError(status_code=404)
        bookings = Booking.query.filter_by(user_id = userID).all()
        return bookings
    
class Venues(Resource):
    @marshal_with(resource_venue)
    def get(self,userID):
        venues = Venue.query.filter_by(admin_id = userID).all()
        if Admin.query.filter_by(user_id = userID).first() is None:
            raise NotFoundError(status_code=404)
        return venues
    
class Shows(Resource):
    @marshal_with(resource_show)
    def get(self,userID):
        shows = Show.query.filter_by(admin_id = userID).all()
        if Admin.query.filter_by(user_id = userID).first() is None:
            raise NotFoundError(status_code=404)
        return shows