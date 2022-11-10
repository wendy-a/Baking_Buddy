from flaskapp import application
from flaskapp.controller import dashboard, landing, recipe_chef, recipe_learner


if __name__ == '__main__':
    application.run()
