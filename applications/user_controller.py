from main import app 
from flask import render_template,request,url_for,redirect
from datetime import datetime
from flask_login import login_required, current_user
from .models import *
from .database import db

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/cancel_confirmation')
@login_required
def cancel_confirmation():
    return render_template('cancel_sucessfully.html')

@app.route("/cancel_booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(booking_id = booking_id).first()
    Show.query.filter_by(show_id = booking.show_id).update({'rseats': booking.tickets_booked + booking.show.rseats})
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('cancel_confirmation'))

@app.route('/booking_history')
@login_required
def booking_history():
    return render_template('booking_history.html',today=datetime.utcnow())

@app.route('/book/<int:show_id>',methods=['GET','POST'])
@login_required
def book(show_id):
    show = Show.query.filter_by(show_id=show_id).first()
    if request.method=='GET':
        return render_template('book_show.html',show=show)
    else:
        ticket_size=request.form.get('ticket_size','')

        try:
            ticket_size=int(ticket_size)
        except:
            return render_template('book_show.html',show=show,error_msg='Invalid Ticket Size!!')

        show = Show.query.filter_by(show_id=show_id).first()
        if show.rseats is None:
            show.rseats = show.venues.capacity

        if ticket_size > show.rseats:
            return render_template('book_show.html',show=show,error_msg=f'{ticket_size} seats are not available!! Remaing seats are {show.rseats}')

        try:
            booking = Booking(user_id = current_user.user_id,
                                show_id = show.show_id,
                                tickets_booked=ticket_size,
                                price_paid = ticket_size * show.ticket_price)
            Show.query.filter_by(show_id=show_id).update({'rseats':show.rseats - ticket_size})
            db.session.add(booking)
            db.session.commit()
        except:
            return render_template('book_show.html',show=show,error_msg='Something went wrong!')
        
        return render_template('booking_success.html',booking=booking)

@app.route("/user")
@login_required
def user_home():
    shows = Show.query.filter(Show.timing >= datetime.utcnow()).all()
    return render_template('home.html',shows=shows)

@app.route('/search_venues',methods=['GET','POST'])
@login_required
def search_venues():
    if request.method=='GET':
        venues = Venue.query.all()
        return render_template('search_venue.html',venues=venues)
    else:
        loc_search = request.form.get('loc_search','')
        venues = Venue.query.filter(Venue.location.contains(loc_search)).all()
        return render_template('search_venue.html',venues=venues,error_msg=f'No Venues Found!! you have searched for location: {loc_search}')


@app.route('/venue_details/<int:venue_id>')
@login_required
def venue_details(venue_id):
    venue = Venue.query.filter_by(venue_id = venue_id).first()
    return render_template('venue_details.html',venue=venue,today=datetime.utcnow())

@app.route('/search_shows',methods=['GET','POST'])
@login_required
def search_shows():
    if request.method=='GET':
        return render_template('search_shows.html')
    else:
        name_search = request.form.get('name_search','')
        rating_search = request.form.get('rating_search','')
        tag_search = request.form.get('tag_search','')
        shows = Show.query.filter(Show.timing >= datetime.utcnow())
        try:
            if name_search != "" and rating_search != "" and tag_search != '':
                shows = shows.filter(Show.rating.between(float(rating_search)-1,float(rating_search)+1)).filter(Show.show_name == name_search).filter(Show.tags.contains(tag_search.upper())).all()
            elif name_search != "" and rating_search != "":
                shows = shows.filter(Show.rating.between(float(rating_search)-1,float(rating_search)+1)).filter(Show.show_name == name_search).all()
            elif rating_search != "" and tag_search != '':
                shows = shows.filter(Show.rating.between(float(rating_search)-1,float(rating_search)+1)).filter(Show.tags.contains(tag_search.upper())).all()
            elif name_search != "" and tag_search != '':
                shows = shows.filter(Show.show_name == name_search).filter(Show.tags.contains(tag_search.upper())).all()
            elif name_search != "":
                shows = shows.filter(Show.show_name == name_search).all()
            elif tag_search != '':
                shows = shows.filter(Show.tags.contains(tag_search.upper())).all()
            else:
                shows = shows.filter(Show.rating.between(float(rating_search)-1,float(rating_search)+1)).all()
        except:
            return render_template('search_shows.html',error_msg='Something went wrong!')

        return render_template('search_shows.html',shows=shows,error_msg='No Show found!!')
    
 