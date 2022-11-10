from flaskapp import application
from flask import render_template, session, redirect, request, flash
from flaskapp.model.recipe import Recipe
from flaskapp.model.user import User
from flaskapp.utility.validator import Validation
from flaskapp.utility.helper import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@application.route('/myRecipe')
def myRecipe():
    user_id = session.get("key", "")
    print(user_id)
    if user_id == "":
        return redirect("/")
    data = {
        "id": user_id
    }
    user = User.get_one(data)
    recipe = Recipe.get_by_user(data)
    return render_template("myRecipe.html", user=user, recipe=recipe)


@application.route('/myRecipe/new')
def create():
    user_id = session.get("key", "")
    if user_id == "":
        return redirect("/")
    data = {
        "id": user_id
    }
    print(user_id)
    user = User.get_one(data)
    return render_template("create_recipe.html", user=user)


@application.route('/create_recipe', methods=["POST"])
def create_recipe():
    if not Validation.validate_recipe(request.form):
        return redirect('/myRecipe/new')
    if not Validation.validate_image(request.files):
        return redirect('/myRecipe/new')


    print(request.form)
    # upload file to s3
    file = request.files['photo']
    if file and allowed_file(file.filename):
        filename = upload_file_to_s3(file)
        if filename == "":
            flash("Upload failure, please try again.", "create")
            return redirect('/myRecipe/new')
    else:
        flash("File type not accepted,please try again.", "create")
        return redirect('/myRecipe/new')

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "ingredient": request.form["ingredient"],
        "instruction": request.form["instruction"],
        "time": int(request.form["time"]),
        "photo": filename,
        "users_id": session.get("key", "")
    }
    print(data)
    Recipe.save(data)
    return redirect("/myRecipe")


@application.route('/myRecipe/edit/<id>')
def view_edit_recipes(id):
    user_id = session.get("key", "")
    if user_id == "":
        return redirect("/")
    data = {
        "id": id
    }
    r = Recipe.get_one(data)
    return render_template("edit_receipt.html", r=r)


@application.route('/edit_recipe/<id>', methods=["POST"])
def edit_recipe(id):  # put application's code here
    if not Validation.validate_recipe(request.form):
        return redirect('/myRecipe/edit/' + id)

    data = {
        "id": id
    }
    r = Recipe.get_one(data)
    file = request.files['photo']
    print(file)
    if file.filename == "":
        filename = r.photo
    else:
        if allowed_file(file.filename):
            filename = upload_file_to_s3(file)
            if filename == "":
                flash("Upload failure, please try again.", "create")
                return redirect('/myRecipe/edit/' + id)
        else:
            flash("Image is not valid.", "create")
            return redirect('/myRecipe/edit/' + id)


    print(request.form)
    data = {
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "ingredient": request.form["ingredient"],
        "instruction": request.form["instruction"],
        "time": request.form["time"],
        "photo": filename
    }
    print(data)
    Recipe.update_one(data)
    return redirect("/myRecipe")


@application.route('/myRecipe/delete/<id>')
def delete_recipe(id):
    data = {
        "id": id
    }
    print(data)
    Recipe.delete_one(data)
    return redirect('/myRecipe')


# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
