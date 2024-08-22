from admin.admin_bp import admin_bp
from flask import request,render_template,redirect,url_for
from flask_login import login_user,logout_user,current_user,login_required
from flask_bcrypt import Bcrypt
from applications.database import db
from applications.models import Admin

bcrypt = Bcrypt()

# @login_manager.user_loader
# def load_user(user_id):
#     return Admin.query.get(user_id)


@admin_bp.route('/login',methods=['GET','POST'])
def admin_login():
    if request.method=='GET':
        return render_template('admin_login.html')
    elif request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username=="" or password=="":
            return render_template('admin_login.html',error_msg='Incorrect Username/Password')
        else:
            user = Admin.query.filter_by(user_id = username).first()
            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect('home')
            else:
                return render_template('admin_login.html',error_msg='Incorrect Username/Password')
            
@admin_bp.route('/logout',methods=['GET','POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect('login')

@admin_bp.route("/register",methods=['GET','POST'])
def admin_register():
    if request.method=='GET':
        return render_template('admin_register.html')
    elif request.method=='POST':
        name = request.form.get('name','')
        email_id = request.form.get('email_id','')
        phone_no = request.form.get('phone_no','')
        username = request.form.get('username','')
        form_password = request.form.get('password','')
        
        
        if Admin.query.filter_by(user_id=username).first():
            return render_template("admin_register.html",error_msg="Username already exits!! Choose different Username")
        
        if len(username) <=4 :
            return render_template("admin_register.html",error_msg="Username should be atleast 5 digit long!!")
        
        try:
           if len(phone_no) != 10:
               raise ValueError
           phone_no = int(phone_no)
        except:
            return render_template("admin_register.html",error_msg="Invalid Phone Number!! Phone Number should be a 10 digit number")
        
        if '@' not in email_id :
            return render_template("admin_register.html",error_msg="Enter a valid email id!!")

        if len(form_password) < 4:
            return render_template("admin_register.html",error_msg="Password should be atleast 4 digit long!!")
        password = bcrypt.generate_password_hash(form_password)
        
        
        new_user = Admin(name=name,
                        email_id = email_id,
                        phone_no=phone_no,
                        user_id=username,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('admin_register_confirmation.html')