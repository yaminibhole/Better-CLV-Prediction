from flask import Blueprint, render_template, redirect, request, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
# from app import get_db  # Ensure this import is correct based on your project structure
# from db import get_db, close_db


user_bp = Blueprint("users", __name__, template_folder="templates")

@user_bp.route("/helloworld")
def helloworld():
    return render_template("hellowold.html")

# @user_bp.route('/login', methods=['GET', 'POST'])
# def login_page():
#     db, cursor = get_db()  # Get the db and cursor from the context
#     if request.method == 'POST':
#         email = request.form.get("mail")
#         password = request.form.get("user-password")
        
#         # Search by email in the database
#         cursor.execute("SELECT * FROM `users` WHERE `email` = %s", (email,))
#         user = cursor.fetchone()
        
#         if user:
#             if check_password_hash(user[4], password):
#                 session["user_id"] = user[0]
#                 session.permanent = True
#                 return redirect('/home')
#             else:
#                 flash("Kindly Check Your Password", 'error')
#         else:
#             flash("Kindly Login First")
        
#     return render_template("users/login.html")

# @user_bp.route('/signup', methods=['GET', 'POST'])
# def signup_page():
#     db, cursor = get_db()  # Get the db and cursor from the context
#     if request.method == 'POST':
#         name = request.form.get("f-name")
#         email = request.form.get("mail")
#         username = request.form.get("u-name")
#         password = generate_password_hash(
#             request.form.get("user-password"),
#             method='pbkdf2:sha256',
#             salt_length=8
#         )
#         phone = int(request.form.get("phone"))

#         # Insert the new user into the database
#         query = """INSERT INTO users (name, username, email, password, phone) VALUES (%s, %s, %s, %s, %s)"""
#         values = (name, username, email, password, phone)
        
#         cursor.execute(query, values)
#         db.commit()

    #     # Sign in the new user
    #     cursor.execute("SELECT * FROM `users` WHERE `email` = %s", (email,))
    #     myuser = cursor.fetchall()
        
    #     if myuser:
    #         session['user_id'] = myuser[0][0]
    #         session.permanent = True
    #         return redirect('/home')
    #     else:
    #         flash("There was an error signing up. Please try again.", 'error')
        
    # return render_template('users/signup.html')
