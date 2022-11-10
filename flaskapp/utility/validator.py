from flaskapp import application
from flaskapp.model.user import User
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(application)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# register validator
class Validation:
    @staticmethod
    def validate_register(user_register):
        is_valid = True  # we assume this is true
        if (not NAME_REGEX.match(user_register['name'])) or len(user_register['name']) < 2:
            flash("Name must be letter only and at least 2 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user_register['email']):
            flash("Email is not Valid", 'register')
            is_valid = False
        if len(user_register['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        if user_register['password'] != user_register['password_two']:
            flash("Password Confirmation doesn't matches password", 'register')
            is_valid = False
        return is_valid

    # log-in validator
    @staticmethod
    def validate_login(user_login):
        if not EMAIL_REGEX.match(user_login['email']):
            flash("Please provide valid Email", 'login')
            return False

        data = {
            "email": user_login["email"]
        }
        user_in_db = User.get_by_email(data)

        if not user_in_db:
            flash("Invalid Email/Password", "login")
            print("email not found")
            return False
        if not bcrypt.check_password_hash(user_in_db.password, user_login['password']):
            flash("Invalid Email/Password", "login")
            print(user_login['password'])
            print("password incorrect")
            return False
        return user_in_db

    # recipe validator
    @staticmethod
    def validate_recipe(recipe_info):
        print(recipe_info)
        is_valid = True
        if len(recipe_info['name']) < 3:
            flash("Name must be at least 3 characters.", 'create')
            is_valid = False
        if len(recipe_info['description']) < 3:
            flash("description must be at least 3 characters.", 'create')
            is_valid = False
        if len(recipe_info['instruction']) < 3:
            flash("instruction must be at least 3 characters.", 'create')
            is_valid = False
        if len(recipe_info['ingredient']) < 3:
            flash("ingredient must be at least 3 characters.", 'create')
            is_valid = False
        if not recipe_info['time']:
            flash("All field must be filled out", 'create')
            is_valid = False
        if "" == recipe_info.get('photo', ""):
            flash("All field must be filled out", 'create')
        return is_valid

    @staticmethod
    def validate_image(image_file):
        is_valid = True
        if 'photo' not in image_file:
            flash('No photo', 'create')
            is_valid = False

        # after confirm 'photo' exist, get the file from input
        file = image_file['photo']

        # check whether a file is selected
        if file.filename == '':
            flash('No photo', 'create')
            is_valid = False
        return is_valid
