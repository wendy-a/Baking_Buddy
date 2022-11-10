from flaskapp import application
from flask import render_template, session, redirect
from flaskapp.model.user import User
from flaskapp.model.recipe import Recipe

@application.route('/dashboard')
def dashboard():
    user_id = session.get("key","")
    print(user_id)
    if user_id == "":
        return redirect("/")
    data = {
        "id": user_id
    }
    user = User.get_one(data)
    recipe = Recipe.get_all()
    return render_template("dashboard.html", user=user, recipe=recipe)


@application.route('/logout')
def logout():
    session["key"] = ""
    return redirect("/")