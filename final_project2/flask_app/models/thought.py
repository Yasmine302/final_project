from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re 

class Thought:
    DB = 'star_war'
    def __init__(self,data):
        self.id = data['id']
        self.title_show = data['title_show']
        self.comment = data['comment']
        self.num_stars = data ['num_stars']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        self.users = []
        self.user = None
        
        
    @classmethod 
    def save(cls, data):
        query = "INSERT INTO thoughts (title_show, comment, num_stars, user_id) VALUES (%(title_show)s, %(comment)s, %(num_stars)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data) 
        
    
    @classmethod
    def delete_by_id(cls, thought_id):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        data = {
            'id': thought_id
        }
        results = connectToMySQL(cls.DB).query_db(query,thought_id)
        return results
    
    @classmethod
    def update(cls,data):
        query = "UPDATE thoughts SET title_show = %(title_show)s,  comment = %(comment)s, num_stars = %(num_stars)s,user_id = %(user_id)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
        
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM thoughts JOIN users ON thoughts.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        thoughts = []
        for thought_dict in results:
            thought_obj = Thought(thought_dict)
            user_obj = user.User({
                'id' : thought_dict['users.id'],
                'first_name' : thought_dict['first_name'],
                'last_name' : thought_dict['last_name'],
                'email' : thought_dict['email'],
                'password' : thought_dict['password'],
                'created_at' : thought_dict['users.created_at'],
                'updated_at' : thought_dict['users.updated_at']
            })
            thought_obj.user = user_obj
            thoughts.append(thought_obj)
        return thoughts
    
    @classmethod 
    def get_one_by_id(cls,thought_id):
        query = "SELECT * FROM thoughts JOIN users ON thoughts.user_id = users.id WHERE thoughts.id = %(id)s;"
        data = {
            'id': thought_id
        }
        thought_dict = connectToMySQL(cls.DB).query_db(query,data)[0]
        thought_obj = Thought(thought_dict)
        user_obj = user.User({
            'id' : thought_dict['users.id'],
            'first_name' : thought_dict['first_name'],
            'last_name' : thought_dict['last_name'],
            'email' : thought_dict['email'],
            'password' : thought_dict['password'],
            'created_at' : thought_dict['users.created_at'],
            'updated_at' : thought_dict['users.updated_at']
        })
        thought_obj.user = user_obj
        return thought_obj
    
    @staticmethod
    def is_valid(thought_dict):
        valid = True
        if len(thought_dict['title_show']) == 0:
            valid = False
            flash("Title of show is required!")
        elif len(thought_dict['title_show']) <= 3:
            valid = False
            flash(" Show must have at least 3 characters!")
        if int(thought_dict['num_stars']) == 0:
            valid = False
            flash("Stars are required!")
        elif int(thought_dict['num_stars']) > 10: 
            flash("Max Stars is 10!")
            valid = False
        if len(thought_dict['comment']) == 0:
            valid = False
            flash("thought is required!")
        elif len(thought_dict['comment']) <= 3:
            valid = False
            flash(" Thought must have at least 3 characters!")
        return valid