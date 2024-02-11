from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.customer import Customer # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller
@app.route('/create', methods=['POST'])
def create_user():
    if not Customer.validate_user(request.form):
        # redirect to the route.
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
        # redirect to the route.
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



