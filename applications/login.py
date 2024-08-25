from main import login_manager,app
import flask
from flask import request,render_template,redirect,url_for
from flask_login import login_user,logout_user,current_user,login_required
from flask_bcrypt import Bcrypt
# from .user_controller import user_home
from .models import User,Admin
from .database import db

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    x =  User.query.get(user_id)
    if x==None:
        x = Admin.query.get(user_id)
    return x

@app.route('/login',methods=['GET','POST'])
def user_login():
    if request.method=='GET':
        return render_template('user_login.html')
    elif request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username=="" or password=="":
            return render_template('user_login.html',error_msg='Incorrect Username/Password')
        else:
            user = User.query.filter_by(user_id = username).first()
            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect('user')
            else:
                return render_template('user_login.html',error_msg='Incorrect Username/Password')

@app.route('/logout',methods=['GET','POST'])
@login_required
def user_logout():
    logout_user()
    return redirect('login')

@app.route("/register",methods=['GET','POST'])
def user_register():
    if request.method=='GET':
        return render_template('user_register.html')
    elif request.method=='POST':
        name = request.form.get('name','')
        email_id = request.form.get('email_id','')
        phone_no = request.form.get('phone_no','')
        address = request.form.get('address',"")
        username = request.form.get('username','')
        form_password = request.form.get('password','')
        
        
        if User.query.filter_by(user_id=username).first():
            return render_template("user_register.html",error_msg="Username already exits!! Choose different Username")
        
        if len(username) <=4 :
            return render_template("user_register.html",error_msg="Username should be atleast 5 digit long!!")
        
        if '@' not in email_id :
            return render_template("user_register.html",error_msg="Enter a valid email id!!")

        try:
           if len(phone_no) != 10:
               raise ValueError
           phone_no = int(phone_no)
        except:
            return render_template("user_register.html",error_msg="Invalid Phone Number!! Phone Number should be a 10 digit number")
        
        if len(form_password) < 4:
            return render_template("user_register.html",error_msg="Password should be atleast 4 digit long!!")
        
        password = bcrypt.generate_password_hash(form_password)

        new_user = User(name=name,
                            email_id = email_id,
                            phone_no=phone_no,
                            address=address,
                            user_id=username,
                            password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('register_confirmation.html')
    
    