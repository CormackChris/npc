from flask_app import app
from flask_app.controllers import controllers_characters, controllers_routes, controllers_users
import pymongo
if __name__=='__main__':
    app.run(debug=True)