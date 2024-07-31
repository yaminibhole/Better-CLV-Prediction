from flask import Flask, render_template, request, flash, url_for, redirect,session,jsonify
from flask_bootstrap import Bootstrap
from controller.user_controller import login_page_controller
from werkzeug.security import generate_password_hash, check_password_hash
# from forms import RegisterUser,LoginUser
from functools import wraps
from datetime import timedelta
import mysql.connector
import os



# ALL Intilization Here 

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


app.secret_key= os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)
conn = mysql.connector.connect(host="127.0.0.1", user="root",password="admin",database="CLVP")
cursor = conn.cursor()




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
                print(session["user_id"])
                return render_template("temp.html",user = user)
            else:
                return jsonify({"error":"SomeThing Is Missing here"})
        else:
           return jsonify({"error": "User not found"}), 404
        
    return render_template("login.html")



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
        return render_template('temp.html',user = myuser)
 

        
    return render_template('signup.html')


@app.route("/")
def home_page():
    # if(session["user_id"]):
    #     cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session["user_id"]))
    #     user= cursor.fetchall()
    #     return render_template("temp.html",user=user)

    return render_template("temp.html")

# LOG OUT
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)