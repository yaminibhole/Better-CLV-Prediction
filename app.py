from flask import Flask, render_template, request, flash, url_for, redirect,session,jsonify
from flask_bootstrap import Bootstrap
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'controller')))
from user_controller import helloWOrld
from werkzeug.security import generate_password_hash, check_password_hash
# from forms import RegisterUser,LoginUser
from functools import wraps
from datetime import timedelta
import mysql.connector
from dotenv import load_dotenv
from blueprints.users.users import user_bp



# ALL Intilization Here 
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("MY_SECRET")
Bootstrap(app)


app.secret_key= os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)
conn = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),database=os.getenv("DB_DETABASE"))
cursor = conn.cursor()


@app.errorhandler(404)
def not_found(error):
    return render_template('clv_pages/error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500
# For Loggin Here 
@app.route('/login',methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        email =  request.form.get("mail")
        password = request.form.get("user-password")
        
        print(email)

        # here Login Search By Email Is Done
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        user= cursor.fetchall()
        print(f"ther user id is :  {user[0][4]}")
        if user:
            if(check_password_hash(user[0][4], password)):
                session["user_id"] = user[0][0]
                # Here Is How I Will Get Session Id
                session.permanent=True
                return redirect('/home')
            else:
                flash("Kindly Check Your Password", 'error')
        else:
           flash("Kindly Login First")
        
    return render_template("users/login.html")



# Sign Up Page Route
@app.route('/signup',methods = ['GET','POST'])
def signup_page():
    if request.method == 'POST':
        name = request.form.get("f-name")
        email =  request.form.get("mail")
        username= request.form.get("u-name")
        password = generate_password_hash(
                request.form.get("user-password"),
                        method='pbkdf2:sha256',
                        salt_length=8
                    )
        phone = int(request.form.get("phone"))
        # Here Query Of Insertion Take Place
        query = """INSERT INTO users (name, username, email, password, phone) VALUES (%s, %s, %s, %s, %s)"""
        values = (name, username, email, password, phone)
        
        cursor.execute(query, values)
        conn.commit()

        # Sign in in site
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        myuser = cursor.fetchall()
        print(myuser)
        session['user_id'] = myuser[0][0]
        session.permanent=True
        return redirect('/home')
 

        
    return render_template('users/signup.html')

@app.route("/teasting")
def teasting():
    # print("hello World")
    # print(session)
    # if 'user_id' in session:
    #     cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
    #     myuser = cursor.fetchall()
    #     return render_template("form.html")
    # return render_template("temp.html")
    return render_template('clv_pages/home.html')

@app.route("/home")
def my_home():
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        print(myuser)
        return render_template("clv_pages/home.html",user = myuser)
    return render_template("index.html")

# Profile Model
@app.route("/myprofile")
def my_profile():  
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        print(myuser)
        return render_template("clv_pages/profile.html",user = myuser)
    return render_template("index.html")

# DashBoard
@app.route("/dashbord")
def dashbord_page():
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        print(myuser)
        return render_template("clv_pages/dashbord.html",user = myuser)
    return render_template('index.html')


# Home app 
@app.route("/homeDevelopment")
def dev():
    return render_template('clv_pages/example[1].html')

app.register_blueprint(user_bp)

# @app.route("/helloworld")
# def hello():
#     return helloWOrld()

#index Page
@app.route("/")
def home_page():
    return render_template("index.html")




# LOG OUT
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)