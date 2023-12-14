from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.customer import Customer # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller
@app.route('/create', methods=['POST'])
def create_user():
    if not Customer.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/new/order')
    # else no errors:
    user_id= Customer.save(request.form)
    return redirect("/cookies")

# Read Users Controller
@app.route('/cookies')
def get_all_orders():
    all_orders = Customer.get_all_customers_orders()
    return render_template("cookies.html", all_orders = all_orders)

@app.route('/new/order')
def show_new_order_page():
    return render_template("new_order.html",)

@app.route('/edit/<int:id>')
def edit(id):
    return render_template('edit_order.html', user=Customer.get_one_user(id))

# Update Users Controller
@app.route('/update/<int:id>',methods=['POST'])
def update_user(id):
    if not Customer.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect(f'/edit/{id}')
    # else no errors:
    user_dict = {
        "customer_name": request.form["customer_name"],
        "cookie_type": request.form["cookie_type"],
        "number_of_boxes":request.form["number_of_boxes"],
        "id":id
        }
    Customer.update(user_dict)
    return redirect('/cookies')


# Delete Users Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.