from flask import Flask

application = app = Flask(__name__)

application.secret_key = "key"