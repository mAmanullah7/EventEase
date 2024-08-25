from flask import render_template,request, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from admin.admin_bp import admin_bp
from applications.models import *
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('AGG')
import os

@admin_bp.route('/summary')
@login_required
def summary():
    graphs=[]
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    tot_revenue = 0
    tot_util = 0
    revenue_per_venue = {}
    capacityUtil_per_venue = {}
    for venue in current_user.venues:
        revenue = 0
        Util = 0
        for show in venue.shows:
            for booking in show.bookings:
                revenue += booking.price_paid
                Util+=booking.tickets_booked
        revenue_per_venue[str(venue.venue_id)]=revenue
        capacityUtil_per_venue[str(venue.venue_id)]=Util
        tot_revenue+=revenue
        tot_util+=Util
    
    revenue_per_show = {}
    capacityUtil_per_show = {}
    for show in current_user.shows:
        revenue = 0
        Util = 0
        for booking in show.bookings:
            revenue += booking.price_paid
            Util+=booking.tickets_booked
        revenue_per_show[str(show.show_id)]=revenue
        capacityUtil_per_show[str(show.show_id)]=Util
    # print(capacityUtil_per_show,capacityUtil_per_venue,revenue_per_show,revenue_per_venue)

    if len(revenue_per_venue) != 0: 
        fig0,ax0=plt.subplots()
        ax0.bar(revenue_per_venue.keys(),revenue_per_venue.values())
        ax0.set_ylabel('Generated Revenue')
        ax0.set_xlabel('Venue ID')
        ax0.set_title("Generated Revenue from each Venue")
        graph_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/graphs','revenue_per_venue.jpg'))
        plt.savefig(graph_img_url)
        # plt.show()
        graphs.append('revenue_per_venue.jpg')

    if len(revenue_per_show) != 0 :
        fig1,ax1 = plt.subplots()
        ax1.bar(revenue_per_show.keys(),revenue_per_show.values())
        ax1.set_ylabel('Generated Revenue')
        ax1.set_xlabel('Show ID')
        ax1.set_title("Generated Revenue from each Show")
        graph_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/graphs','revenue_per_show.jpg'))
        plt.savefig(graph_img_url)
        # plt.show()
        graphs.append('revenue_per_show.jpg')

    if len(capacityUtil_per_show) != 0:
        fig3,ax3 = plt.subplots()
        ax3.bar(capacityUtil_per_show.keys(),capacityUtil_per_show.values())
        ax3.set_ylabel('Capacity Utilization')
        ax3.set_xlabel('Show ID')
        ax3.set_title("Capacity Utilization from each Show")
        graph_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/graphs','capacity_per_show.jpg'))
        plt.savefig(graph_img_url)
        # plt.show()
        graphs.append('capacity_per_show.jpg')

    if len(capacityUtil_per_venue) != 0:
        fig4,ax4=plt.subplots()
        ax4.bar(capacityUtil_per_venue.keys(),capacityUtil_per_venue.values())
        ax4.set_ylabel('Capacity Utilization')
        ax4.set_xlabel('Venue ID')
        ax4.set_title("Capacity Utilization from each Venue")
        plt.xticks(rotation=10)
        graph_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/graphs','capacity_per_venue.jpg'))
        plt.savefig(graph_img_url)
        # plt.show()
        graphs.append('capacity_per_venue.jpg')

    return render_template('summary.html',graphs=graphs,revenue=tot_revenue,util=tot_util)

@admin_bp.route("/delete_show/<int:show_id>")
@login_required
def delete_show(show_id):
    show_details = Show.query.filter_by(show_id = show_id).first()
    return render_template('deleteShow_confirmation.html',show = show_details)

@admin_bp.route("/delete_show/<int:show_id>/confirm")
@login_required
def delete_show_confirm(show_id):
    shows=Show.query.filter_by(show_id = show_id).all()
    for show in shows:
        db.session.delete(show)
    db.session.commit()
    return redirect(url_for('admin.index'))

@admin_bp.route("/edit_venue/<int:venue_id>",methods=['GET','POST'])
@login_required
def edit_venue(venue_id):
    if request.method=='GET':
        venue_details = Venue.query.filter_by(venue_id = venue_id).first()
        return render_template('edit_venue.html',venue = venue_details)
    else:
        name = request.form.get('name','')
        location = request.form.get('location','')
        capacity=request.form.get('capacity',"")
        address = request.form.get("address",'')

        if name=='' or name==' ':
            return render_template('admin_venue_new.html',error_msg = "Invalid venue name!! Enter correct venue name")
        
        if location==' ' or location=='':
            return render_template('admin_venue_new.html',error_msg = "Invalid Location!! Enter correct location")
        
        try:
            capacity = int(capacity)
            if capacity<=0:
                raise ValueError
        except:
            return render_template('admin_venue_new.html',error_msg = "Invalid Capacity!! Capacity of venue should be greater than 0.")
        

        venue_img_url = ''
        try:
            image = request.files['image']
            if image.filename != '':
                file_name = secure_filename(name+"_venueimg_" + image.filename)
                curr_dir = os.path.abspath(os.path.dirname(__file__))
                venue_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/venue_img',file_name))
                image.save(venue_img_url)
        except:
            return render_template('admin_venue_new.html',error_msg = "Something went wrong with uploading image!! Try Again")
            

        try:
            Venue.query.filter_by(venue_id=venue_id).update({'venue_name' : name,
                                                            'location' : location,
                                                            'address' : address,
                                                            'capacity':capacity,
                                                            'venue_img_url': venue_img_url})
            db.session.commit()
        except:
            return render_template('admin_venue_new.html',error_msg = "Something went wrong!! Try Again")
        
        return render_template('edit_success.html',option='Venue')

@admin_bp.route("/delete_venue/<int:venue_id>")
@login_required
def delete_venue(venue_id):
    venue_details = Venue.query.filter_by(venue_id = venue_id).first()
    return render_template('deleteVenue_confirmation.html',venue = venue_details)

@admin_bp.route("/delete_venue/<int:venue_id>/confirm")
@login_required
def delete_venue_confirm(venue_id):

    shows = Show.query.filter_by(venue_id = venue_id).all()
    for show in shows:
        db.session.delete(show)

    venues = Venue.query.filter_by(venue_id=venue_id).all()
    for venue in venues:
        db.session.delete(venue)
    db.session.commit()
    return redirect(url_for('admin.index'))


@admin_bp.route("/home")
@login_required
def index():
    return render_template('admin_homepage.html')

@admin_bp.route("/add_venue",methods=['GET','POST'])
@login_required
def add_venue():
    if request.method == 'GET':
        return render_template('admin_venue_new.html')
    else:
        name = request.form.get('name','')
        location = request.form.get('location','')
        capacity=request.form.get('capacity',"")
        address = request.form.get("address",'')

        if name=='' or name==' ':
            return render_template('admin_venue_new.html',error_msg = "Invalid venue name!! Enter correct venue name")
        
        if location==' ' or location=='':
            return render_template('admin_venue_new.html',error_msg = "Invalid Location!! Enter correct location")
        
        try:
            capacity = int(capacity)
            if capacity<=0:
                raise ValueError
        except:
            return render_template('admin_venue_new.html',error_msg = "Invalid Capacity!! Capacity of venue should be greater than 0.")
        

        venue_img_url = ''
        try:
            image = request.files['image']
            if image.filename != '':
                file_name = secure_filename(name+"_venueimg_" + image.filename)
                curr_dir = os.path.abspath(os.path.dirname(__file__))
                venue_img_url = os.path.normpath(os.path.join(curr_dir,'../../static/images/venue_img',file_name))
                image.save(venue_img_url)
        except:
            return render_template('admin_venue_new.html',error_msg = "Something went wrong with uploading image!! Try Again")
            

        try:
            new_venue = Venue(venue_name = name,
                              location = location,
                              address = address,
                              capacity=capacity,
                              admin_id=current_user.user_id,
                              venue_img_url=venue_img_url)
            db.session.add(new_venue)
            db.session.commit()
        except:
            return render_template('admin_venue_new.html',error_msg = "Something went wrong!! Try Again")
        
        return render_template('venue_added.html')
   

@admin_bp.route("/add_show",methods=['GET','POST'])
@login_required
def add_show():
    if request.method == 'GET':
        return render_template('admin_newShow.html')
    else:
        name = request.form.get("name","")
        description = request.form.get("description","")
        action = request.form.get("action","")
        comedy = request.form.get("comedy","")
        drama  = request.form.get("drama","") 
        romance = request.form.get("romance","")
        thriller =request.form.get("thriller","")
        venue=request.form.getlist("venue")
        price = request.form.get("price","")
        timing=request.form.get("timing","")
        rating=request.form.get("rating","")
        
        if len(venue) == 0 :
            return render_template("admin_newShow.html",error_msg = "Select atleast one venue for hosting shows")
        
        if len(name)<=4:
            return render_template("admin_newShow.html",error_msg = "Show name should have length greater than 4")
        
        if len(description)<=15:
            return render_template("admin_newShow.html",error_msg = "Description should have length greater than 15")
        
        tags=[]

        if action=="action":
            tags.append(action)
        
        if comedy=='comedy':
            tags.append(comedy)
        
        if drama == 'drama':
            tags.append(drama)
        
        if romance == 'romance':
            tags.append(romance)
        
        if thriller=='thriller':
            tags.append(thriller)

        tag = ' '.join(tags)

        try:
            price = float(price)
        except:
            return render_template("admin_newShow.html",error_msg = "Invalid Price")

        try:
            timing = datetime.fromisoformat(timing)
        except:
            return render_template("admin_newShow.html",error_msg = "Something went wrong!! Try Again")
        
        try:
            rating=float(rating)
            if rating>10 or rating<0:
                raise ValueError
        except:
            return render_template("admin_newShow.html",error_msg = "Rating should be between 0 and 10")

        try:
            for i in venue:
                new_show = Show(show_name=name,
                            description=description,
                            tags=tag,
                            venue_id=i,
                            ticket_price=price,
                            admin_id=current_user.user_id,
                            timing=timing,
                            rating=rating)
                db.session.add(new_show)
            db.session.commit()
        except:
            return render_template("admin_newShow.html",error_msg = "Something went wrong!! Try Again")
        return render_template("show_added.html")

@admin_bp.route("/edit_show/<int:show_id>",methods=['GET','POST'])
@login_required
def edit_show(show_id):
    if request.method == 'GET':
        show_details = Show.query.filter_by(show_id = show_id).first()
        return render_template('edit_show.html',show = show_details)
    else:
        name = request.form.get("name","")
        description = request.form.get("description","")
        action = request.form.get("action","")
        comedy = request.form.get("comedy","")
        drama  = request.form.get("drama","") 
        romance = request.form.get("romance","")
        thriller =request.form.get("thriller","")
        # venue=request.form.getlist("venue")
        price = request.form.get("price","")
        timing=request.form.get("timing","")
        rating=request.form.get("rating","")
        
        # if len(venue) == 0 :
        #     return render_template("admin_newShow.html",error_msg = "Select atleast one venue for hosting shows")
        
        if len(name)<=4:
            return render_template("edit_show.html",error_msg = "Show name should have length greater than 4")
        
        if len(description)<=15:
            return render_template("edit_show.html",error_msg = "Description should have length greater than 15")
        
        tags=[]

        if action=="action":
            tags.append(action)
        
        if comedy=='comedy':
            tags.append(comedy)
        
        if drama == 'drama':
            tags.append(drama)
        
        if romance == 'romance':
            tags.append(romance)
        
        if thriller=='thriller':
            tags.append(thriller)

        tag = ' '.join(tags)

        try:
            price = float(price)
        except:
            return render_template("edit_show.html",error_msg = "Invalid Price")

        try:
            timing = datetime.fromisoformat(timing)
        except:
            return render_template("edit_show.html",error_msg = "Something went wrong!! Try Again")
        
        try:
            rating=float(rating)
            if rating>10 or rating<0:
                raise ValueError
        except:
            return render_template("edit_show.html",error_msg = "Rating should be between 0 and 10")
        
        try:
            Show.query.filter_by(show_id = show_id).update({'show_name':name,
                                                            'description':description,
                                                            'tags':tag,
                                                            'ticket_price':price,
                                                            'timing':timing,
                                                            'rating':rating})
            db.session.commit()
        except:
            return render_template("edit_show.html",error_msg = "Something went wrong!! Try Again")
        return render_template("edit_success.html",object='Show')
        
        