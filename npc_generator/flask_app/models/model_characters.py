from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import model_users

class Character:
    def __init__ (self, data):
        self.id = data["id"]
        self.genre = data["genre"]
        self.name = data["name"]
        self.age = data["age"]
        self.role = data["role"]
        self.alignment = data["alignment"]
        self.personality_one = data["personality_one"]
        self.personality_two = data["personality_two"]
        self.personality_three = data["personality_three"]
        self.notes = data["notes"]
        self.gender = data["gender"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data ["user_id"]
        # self.fullname = f"{self.title.capitalize}{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def creator(self):
        return model_users.User.get_one({'id': self.user_id })

    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO characters (genre, name, age, role, alignment, notes, gender, personality_one, personality_two, personality_three, user_id) VALUES (%(genre)s, %(name)s, %(age)s, %(role)s, %(alignment)s, %(notes)s, %(gender)s, %(personality_one)s, %(personality_two)s, %(personality_three)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM characters WHERE id = %(id)s"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM characters;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_characters = []
            for characters in results:
                all_characters.append(cls(characters))
            return all_characters
        return False

    @classmethod 
    def update_one(cls, data:dict) -> None:
        query = "UPDATE characters SET genre = %(genre)s, name = %(name)s, age = %(age)s, gender = %(gender)s, role = %(role)s, alignment = %(alignment)s, notes = %(notes)s, personality_one = %(personality_one)s, personality_two = %(personality_two)s, personality_three = %(personality_three)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, data:dict) -> None:
        query = "DELETE FROM characters WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True

        if len(data["genre"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_genre")

        if len(data["name"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_name")
        
        if len(data["age"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_age")

        if len(data["role"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_role")

        if len(data["alignment"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_alignment")

        if len(data["personality_one"]) < 1:
            is_valid = False 
            flash("field is required", "err_characters_personality")

        return is_valid