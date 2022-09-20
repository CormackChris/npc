from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__ (self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.pw = data["pw"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO users (username, email, pw) VALUES (%(username)s, %(email)s, %(pw)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_username(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) -> list:
        query = "select * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    @classmethod 
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET username = %(username)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True
        if len(data["username"]) < 3:
            is_valid = False
            flash("field is required", "err_user_username")
            
        else:
            potential_user = User.get_one_by_username({'username': data['username']})
            if potential_user:
                flash("Username already exists!", "err_user_username")
                is_valid = False

        if len(data["email"]) < 3:
            is_valid = False
            flash("field is required", "err_user_email")
        
        elif not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid email address!", "err_user_email")
            is_valid = False

        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if potential_user:
                flash("Email address already exists!", "err_user_email")
                is_valid = False

        if len(data["pw"]) < 8:
            is_valid = False
            flash("field is required", "err_user_pw")

        if len(data["confirm_pw"]) < 8:
            is_valid = False
            flash("field is required", "err_user_confirm_pw")

        elif data["pw"] == ["confirm_pw"]:
            is_valid = False
            flash("passwords do not match", "err_user_confirm_pw")
        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if len(data["email"]) < 3:
            is_valid = False
            flash("field is required", "err_user_email_login")
        
        elif not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid email address!", "err_user_email_login")
            is_valid = False

        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if not potential_user:
                flash("Email address doesn't exist!", "err_user_email_login")
                is_valid = False

            else:
                if not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                    flash("Invalid Credentials", "err_user_email_login")
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id

        if len(data["pw"]) < 1:
            is_valid = False
            flash("field is required", "err_user_pw_login")

        return is_valid