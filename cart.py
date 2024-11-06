import json
from flask import Flask, request, render_template, session, url_for, redirect, jsonify

app = Flask(__name__, static_url_path='static')
app.secret_key = "hehehe"

# Load JSON data
with open('db/products.json') as f:
    data = json.load(f)

@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    # 1. Get the product id and quantity from the form
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    # 2. Get the product details from the JSON data
    product = next((item for item in data["products"] if item["ProductId"] == product_id), None)
    if not product:
        return "Product not found", 404

    # 3. Create a dictionary for the product
    product_dict = {
        "id": product_id,
        "name": product["ProductTitle"],
        "price": float(product["Price"].replace("$", "")),
        "quantity": quantity,
        "picture": product["Image"],
        "details": {
            "Category": product["Category"],
            "ProductType": product["ProductType"],
            "Colour": product["Colour"],
            "Usage": product["Usage"]
        }
    }

    # 4. Get the cart from the session or create an empty list
    cart = session.get("cart", [])

    # 5. Check if the product is already in the cart
    found = False
    for item in cart:
        if item["id"] == product_id:
            # Update the quantity of the existing product
            item["quantity"] += quantity
            found = True
            break

    if not found:
        # Add the new product to the cart
        cart.append(product_dict)

    # 6. Save the cart back to the session
    session["cart"] = cart

    # 7. Print out
    rows = len(cart)
    outputmessage = (
        f'"Product added to cart successfully!"'
        f"</br>Current: {rows} products"
        f'</br>Continue Search! <a href="/">Search Page</a>'
        f'</br>View Shopping Cart! <a href="/view_cart">ViewCart</a>'
    )

    return outputmessage

@app.route("/view_cart")
def view_cart():
    # Get the cart from the session or create an empty list
    current_cart = session.get("cart", [])
    current_username = session.get('current_user', {}).get('name', "")
    return render_template("cart_update.html", carts=current_cart, user_name=current_username)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    # Get the shopping cart from the session
    cart = session.get('cart', [])
    # Create a new cart to store updated items
    new_cart = []
    # Iterate over each item in the cart
    for product in cart:
        product_id = str(product['id'])
        # If this product has a new quantity in the form data
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            # If the quantity is 0 or this is a delete field, skip this product
            if quantity == 0 or f'delete-{product_id}' in request.form:
                continue
            # Otherwise, update the quantity of the product
            product['quantity'] = quantity
        # Add the product to the new cart
        new_cart.append(product)
    # Save the updated cart back to the session
    session['cart'] = new_cart
    # Redirect to the shopping cart page
    return redirect(url_for('view_cart'))

@app.route('/proceed_cart', methods=['POST'])
def proceed_cart():
    # Retrieve the user ID from the session
    current_user = session.get('current_user')
    if not current_user:
        return "User not logged in", 403

    user_id = current_user['id']
    user_email = current_user['email']

    # Get the shopping cart from the session
    shopping_cart = session.get("cart", [])

    # Save order information to a dictionary (simulating a database)
    order = {
        "user_id": user_id,
        "user_email": user_email,
        "user_address": "User Address",
        "user_mobile": "User Mobile",
        "purchase_date": "2023-10-10",
        "ship_date": "2023-10-15",
        "status": 1,
        "details": shopping_cart
    }

    # Save order to session (or you can implement another way to store this)
    session['last_order'] = order

    # Remove the cart from the session
    session.pop("cart", None)

    # Redirect to the order page
    order_url = url_for('orders', order_id=1, _external=True)  # Assuming only one order for simplicity
    return f'Redirecting to order page: <a href="{order_url}">{order_url}</a>'

@app.route('/orders/', defaults={'order_id': None}, methods=['GET'])
@app.route('/orders/<int:order_id>/', methods=['GET'])
def orders(order_id):
    current_user = session.get('current_user')
    if not current_user:
        return "User not logged in", 403

    user_id = current_user['id']
    last_order = session.get('last_order')

    if order_id is not None and last_order and last_order["user_id"] == user_id:
        order = last_order
        order_details = last_order["details"]
        return render_template('order_details.html', order=order, order_details=order_details)
    else:
        orders = [last_order] if last_order and last_order["user_id"] == user_id else []
        return render_template('orders.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['txt_username']
        password = request.form['txt_password']
        obj_user = get_obj_user(username, password)
        if obj_user is not None:
            session['current_user'] = {
                "id": obj_user["id"],
                "name": obj_user["name"],
                "email": obj_user["email"]
            }
        return redirect(url_for('index'))
    return render_template('login.html')

def get_obj_user(username, password):
    # Simulate user authentication
    users = [
        {"id": 1, "name": "user1", "email": "user1@example.com", "password": "pass1"},
        {"id": 2, "name": "user2", "email": "user2@example.com", "password": "pass2"}
    ]
    user = next((u for u in users if u["name"] == username and u["password"] == password), None)
    return user

@app.route('/logout')
def logout():
    session.pop('current_user', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return "Index Page"

if __name__ == '__main__':
    app.run(debug=True)
