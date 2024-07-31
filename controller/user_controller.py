from flask import Flask, render_template, request




def login_page_controller():
    if request.method == 'POST':
        email =  request.form.get("mail")
        password = request.form.get("user-password")
        
        # here Login Search By Email Is Done
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
        user= cursor.fetchall()
        print(f"ther user id is :  {user[0][0]}")
        if user:
            session["user_id"] = user[0][0]
            # Here Is How I Will Get Session Id
            session.permanent=True
            print(session["user_id"])
            return render_template("temp.html",user=user)
        else:
           return jsonify({"error": "User not found"}), 404
        
    return render_template("login.html")