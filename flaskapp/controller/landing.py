from flaskapp import application
from flask import render_template, request, redirect, session, flash
from flaskapp.model.user import User
from flaskapp.utility.validator import Validation, bcrypt

@application.route('/')
def landing():
    return render_template("landing.html")


@application.route('/register', methods=["POST"])
def register():
    validation_result = Validation.validate_register(request.form)
    if not validation_result:
        return redirect('/')

    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password": password_hash,
        "isChef": request.form["isChef"] == 'true'
    }
    user_id = User.save(data)
    session["key"] = user_id
    return redirect("/dashboard")


@application.route('/login', methods=["POST"])
def login():
    validation_result = Validation.validate_login(request.form)
    if not validation_result:
        return redirect('/')
    session['key'] = validation_result.id
    return redirect("/dashboard")
