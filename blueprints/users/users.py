from flask import Blueprint,render_template,redirect

user_bp = Blueprint("users",__name__,template_folder="templates")


@user_bp.route("/helloworld")
def helloworld():
    return render_template("hellowold.html")