from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'stuff and things'

bcrypt = Bcrypt(app)
DATABASE  = 'characters_db'