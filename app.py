import os
import pickle
import sys
from datetime import timedelta
# from forms import RegisterUser,LoginUser
from functools import wraps

# cloudinary Import
import cloudinary
import cloudinary.api
import cloudinary.uploader
import google.generativeai as genai
import matplotlib
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_file, session, url_for)
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash

import generate_report
from blueprints.users.users import user_bp
from prediction_methodes import (categorize_customer, generate_recommendation,
                                 generate_visualizations, generation_config,
                                 generation_model, handle_file_requirements,
                                 handle_manual_requirements, model)

# ALL Intilization Here 
load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
matplotlib.use('Agg')
app.config['SECRET_KEY'] = os.getenv("MY_SECRET")
Bootstrap(app)


app.secret_key= os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)
conn = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),database=os.getenv("DB_DETABASE"))
cursor = conn.cursor()


# Cloudinary Config

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECREAT")
)





@app.errorhandler(404)
def not_found(error):
    return render_template('clv_pages/error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500

@app.route('/predict', methods=['GET', 'POST'])
def upload_and_predict():
    if request.method == 'POST':
        file = request.files.get('file')
        particular_id = request.form.get('particular_id')
        use_manual_input = request.form.get('use_manual_input') == 'true'
        if use_manual_input:
            try:
                # Extract features from the form
                features = [
                    float(request.form['paid_late_fees']),
                    float(request.form['debt_to_income']),
                    float(request.form['credit_utilization_ratio']),
                    float(request.form['annual_income']),
                    float(request.form['average_age_of_credit']),
                    float(request.form['loan_to_income_ratio']),
                    float(request.form['employment_stability']),
                    float(request.form['credit_inquiries_trend']),
                    float(request.form['monthly_payment_burden']),
                    float(request.form['paid_principal']),
                    float(request.form['paid_interest']),
                    float(request.form['total_credit_limit']),
                    float(request.form['total_credit_utilized'])
                ]
                balance = float(request.form['balance'])

                # Create a feature array for prediction
                features_array = np.array([features])

                # Make prediction
                prediction = model.predict(features_array)

                # Create a DataFrame for manual input to generate visualizations
                manual_data = pd.DataFrame(features_array, columns=[
                    'paid_late_fees', 'debt_to_income', 'credit_utilization_ratio',
                    'annual_income', 'average_age_of_credit', 'loan_to_income_ratio',
                    'employment_stability', 'credit_inquiries_trend', 'monthly_payment_burden',
                    'paid_principal', 'paid_interest', 'total_credit_limit', 'total_credit_utilized'
                ])
                manual_data['balance'] = balance
                print(f"-----------------The Predictio is : = {prediction}" )
                manual_plot_url1,manual_plot_url2,manual_data_html,recommendation_list = handle_manual_requirements(manual_data=manual_data,prediction=prediction) 

                return redirect("/dashbord")
            except ValueError as e:
                flash("Form Details Not fetch Properly","error")
                return redirect("/home")
            
        elif file and particular_id:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            try:
                particular_id = int(particular_id)
                df = pd.read_csv(file_path)
                filtered_data = df[df['ID'] == particular_id]
                
                if (filtered_data.empty):
                    flash("No data found for the given ID","error")
                    return redirect("/home")
                else:
                    # Extract features for prediction from the filtered data
                    features = filtered_data[['paid_late_fees', 'debt_to_income', 'credit_utilization_ratio',
                                              'annual_income', 'average_age_of_credit', 'loan_to_income_ratio',
                                              'employment_stability', 'credit_inquiries_trend', 'monthly_payment_burden',
                                              'paid_principal', 'paid_interest', 'total_credit_limit', 'total_credit_utilized']].values
                    balance = filtered_data['balance'].values[0]
                    
                    prediction = model.predict(features)
                    print(f"-----------------The Predictio is : = {prediction}" )
                    # Calculate CLV
                    
                    plot_url1,plot_url2,recommendation_list = handle_file_requirements(filtered_data=filtered_data,prediction=prediction)
                    return redirect("/dashbord")
            except ValueError:
                flash("Value Error Occoured","error")
                return redirect("/home")
        else:
            flash("The Parameter Is Not Found","error")

    return redirect("/home")

@app.route("/generate_report")
def gen_report():
    if request.method == 'GET':
        customer_profile = session.get('customer_profile')
        prediction = session.get('prediction')
        recommendation = session.get('recommendation')
        plot_url1=session.get("plt1_path")
        report_path=generate_report.generate_report(customer_profile,prediction,recommendation)
        
        return send_file(report_path, as_attachment=True)
    return render_template("index.html")



# For Loggin Here 
@app.route('/login',methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        email =  request.form.get("mail")
        password = request.form.get("user-password")
        

        # here Login Search By Email Is Done
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        user= cursor.fetchall()
        if user:
            if(check_password_hash(user[0][4], password)):
                session["user_id"] = user[0][0]
                # Here Is How I Will Get Session Id
                session.permanent=True
                return redirect('/home')
            else:
                flash("Kindly Check Your Password", 'danger')
                return render_template("index.html")
        else:
           flash("Kindly Login First",'danger')
        
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
        img = "https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg"
        # Here Query Of Insertion Take Place
        query = """INSERT INTO users (name, username, email, password, phone, img) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (name, username, email, password, phone,img)
        
        cursor.execute(query, values)
        conn.commit()

        # Sign in in site
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        myuser = cursor.fetchall()
        session['user_id'] = myuser[0][0]
        session.permanent=True
        flash("Successfully Loggin Done","error")
        return redirect('/home')
 

        
    return render_template('users/signup.html')


# EDIT IMAGES

@app.route('/edit-image', methods=['POST'])
def edit_image():
    if 'newImage' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['newImage']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result.get('url')
        if "user_id" in session:
            cursor.execute("""
                UPDATE `users` 
                SET `img` = %s 
                WHERE `user_id` = %s
            """, (image_url, session['user_id']))

            # Commit the changes to the database
            conn.commit()
            
        return jsonify({"image_url": image_url}), 200
    
    except Exception as e:
        return jsonify({"error": "Failed to upload image"}), 500




@app.route("/home")
def my_home():
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        return render_template("clv_pages/home.html",user = myuser)
    return render_template("index.html")

# Profile Model
@app.route("/myprofile")
def my_profile():  
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        return render_template("clv_pages/profile.html",user = myuser)
    return render_template("index.html")

# DashBoard
@app.route("/dashbord")
def dashbord_page():
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `users` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
        myuser = cursor.fetchall()
        if "customer_profile" not in session:
            flash(f"please fill the form first !", "error")
            return redirect('/home')

        customer_profile = session.get('customer_profile')
        prediction = session.get('prediction')
        recommendation = session.get('recommendation')

        # Clean up recommendations
        cleaned_recommendation = []
        for rec in recommendation:
            if ":" in rec:
                rec_key_value = rec.split(":", 1)
                rec_key = rec_key_value[0].replace("- **", "").replace("**", "").strip()
                rec_value = rec_key_value[1].replace("**", "").strip()
                cleaned_recommendation.append(f"{rec_key}: {rec_value}")
            else:
                # Handle case where recommendation does not contain a colon
                cleaned_recommendation.append(rec.replace("- **", "").replace("**", "").strip())

        return render_template("clv_pages/dashbord.html", user=myuser, customer_profile=customer_profile, prediction=prediction, recommendation=cleaned_recommendation)
    return render_template('index.html')

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
    app.run(host='0.0.0.0', port=3300, debug=True)