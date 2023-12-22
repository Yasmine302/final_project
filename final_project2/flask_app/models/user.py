from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    DB ='star_war'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password =data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod 
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.DB).query_db(query, data) 
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s,  last_name = %(last_name)s, email = %(email)s,password = %(password)s, user_id = %(user_id)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod 
    def get_by_email(cls,data):
        print(data)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
        
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if not results:
            return None
        return cls(results[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(results) >= 1:
            flash("Email already exists","register")
            is_valid = False
        if len(user['first_name']) == 0:
            flash("First_name is required","register")
            is_valid = False
        elif len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!","register")
            is_valid = False
        if len(user['last_name']) == 0:
            flash("Last name is required","register")
            is_valid = False
        elif len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!","register")
            is_valid = False
        if len(user['email']) == 0: 
            flash('Email is required',"register")
        if len(user['password']) == 0:
            flash('Password is required')
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters!","register")
            is_valid = False
        if len(user['confirm']) == 0: 
            flash("Confirm Password is required","register")
            is_valid = False
        if user['password'] !=  user['confirm']:
            flash("Password must match!!","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Enter Valid Email Address!!","register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(emails)s;"
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(results) < 1: 
            flash("Invalid Email", "login")
            is_valid = False
        return is_valid
    