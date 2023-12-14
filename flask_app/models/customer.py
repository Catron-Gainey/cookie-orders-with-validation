
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
class Customer:
    db = "cookies" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Users Models
    @classmethod
    def save(cls, data):
        query = """INSERT INTO customers (customer_name, cookie_type, number_of_boxes)
                VALUES (%(customer_name)s, %(cookie_type)s, %(number_of_boxes)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    # Read Users Models
    @classmethod
    def get_all_customers_orders(cls):
        query = "SELECT * FROM customers;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('cookies').query_db(query)
        # Create an empty list to append our instances of friends
        orders = []
        # Iterate over the db results and create instances of friends with cls.
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def get_one_user(cls, id):
        query = "SELECT * from customers WHERE id = %(id)s;"
        result = connectToMySQL('cookies').query_db(query, {"id":id})
        print(result)
        return cls(result[0])

    # Update Users Models
    @classmethod
    def update(cls,user_data):
        query = """UPDATE customers 
                SET customer_name=%(customer_name)s,cookie_type=%(cookie_type)s,number_of_boxes=%(number_of_boxes)s
                WHERE id = %(id)s
                ;"""
        return connectToMySQL(cls.db).query_db(query,user_data)

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['customer_name']) < 2:
            flash("first name can't be blank.")
            is_valid = False
        if len(user['cookie_type']) < 2:
            flash("cookie type can't be blank")
            is_valid = False
        if int(user['number_of_boxes']) < 0:
            flash("number of boxes cant be negative.")
            is_valid = False
        return is_valid


    # Delete Users Models