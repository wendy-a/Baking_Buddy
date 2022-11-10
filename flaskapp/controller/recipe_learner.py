from flaskapp import application
from flask import render_template, session, redirect, request, flash
from flaskapp.model.recipe import Recipe
from flaskapp.model.work import Work
from flaskapp.utility.helper import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@application.route('/recipe/<recipe_id>')
def get_recipes(recipe_id):
    user_id = session.get("key", "")
    if user_id == "":
        return redirect("/")

    data = {
        "id": int(recipe_id)
    }
    r = Recipe.get_one(data)

    workData = {
        "id": r.id
    }
    work = Work.get_all_photo(workData)

    return render_template("view_recipe.html", user_id=user_id, r=r, work=work)


@application.route('/recipe_work/<recipe_id>', methods=["POST"])
def upload_work(recipe_id):
    user_id = session.get("key", "")
    if user_id == "":
        return redirect("/")

    file = request.files['photo']
    if file and allowed_file(file.filename):
        filename = upload_file_to_s3(file)
        if filename == "":
            flash("Upload failure, please try again.", "create")
            return redirect("/recipe/"+recipe_id)
    else:
        flash("File type not accepted,please try again.", "create")
        return redirect("/recipe/"+recipe_id)

    data = {
        "photo": filename,
        "recipe_id": int(recipe_id),
        "users_id": session.get("key", "")
    }
    Work.save(data)
    return redirect("/recipe/"+recipe_id)


@application.route('/recipe/<recipe_id>/<work_id>/delete')
def delete_work(recipe_id, work_id):
    data = {
        "id": int(work_id)
    }
    print(data)
    Work.delete_one(data)
    return redirect('/recipe/'+ recipe_id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS