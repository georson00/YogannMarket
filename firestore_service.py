import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import requests


# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore Service Functions
def add_user(user_id, name, email):
    db.collection("users").document(user_id).set({
        "name": name,
        "email": email,
        "created_at": datetime.utcnow().isoformat()
    })


def add_product(product_id, name, price, description, user_id):
    db.collection("products").document(product_id).set({
        "name": name,
        "price": price,
        "description": description,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    })

def update_product(product_id, updated_fields):
    db.collection("products").document(product_id).update(updated_fields)

def delete_product(product_id):
    db.collection("products").document(product_id).delete()

def get_all_products():
    products = db.collection("products").stream()
    found = False
    for product in products:
        data = product.to_dict()
        found = True
        print(f"📦 Product ID: {product.id}")
        print(f"Name       : {data.get('name')}")
        print(f"Price      : ${data.get('price'):.2f}")
        print(f"Description: {data.get('description')}")
        print(f"Created By : {data.get('user_id')}")
        print(f"Date Added : {data.get('created_at')}")
        print("-" * 30)
    if not found:
        print("There are no products available for now.")

def get_products_by_user(user_id):
    products = db.collection("products").where("user_id", "==", user_id).stream()
    found = False
    for product in products:
        found = True
        data = product.to_dict()
        print(f"📦 Product ID: {product.id}")
        print(f"Name       : {data.get('name')}")
        print(f"Price      : ${data.get('price'):.2f}")
        print(f"Description: {data.get('description')}")
        print(f"Created By : {data.get('user_id')}")
        print(f"Date Added : {data.get('created_at')}")
        print("-" * 30)
    if not found:
        print("No products found for this user.")


def get_orders_by_user(user_id):
    orders = db.collection("orders").where("user_id", "==", user_id).stream()
    found = False

    for order in orders:
        found = True
        data = order.to_dict()

        # Format order date
        raw_date = data.get("order_date")
        formatted_date = "N/A"
        if raw_date:
            try:
                formatted_date = datetime.fromisoformat(raw_date).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = raw_date

        # Get product name using product_id
        product_id = data.get("product_id")
        product_name = "Unknown Product"
        if product_id:
            product_ref = db.collection("products").document(product_id)
            product_doc = product_ref.get()
            if product_doc.exists:
                product_data = product_doc.to_dict()
                product_name = product_data.get("name", product_name)

        # Display formatted output
        print("-" * 40)
        print(f"🛒 Order ID   : {order.id}")
        print(f"Product      : {product_name} (ID: {product_id})")
        print(f"Quantity     : {data.get('quantity')}")
        print(f"Total Price  : ${data.get('total_price'):.2f}")
        print(f"Ordered By   : {data.get('user_id')}")
        print(f"Order Date   : {formatted_date}")
        print("-" * 40)

    if not found:
        print("No orders found for this user.")
def add_to_cart(user_id, product_id, quantity):
    # Get product to add to cart
    product_ref = db.collection("products").document(product_id)
    product_doc = product_ref.get()

    if not product_doc.exists:
        print("❌ Product not found.")

    product_data = product_doc.to_dict()
    cart_item_ref = db.collection("users").document(user_id).collection("cart").document(product_id)

    existing = cart_item_ref.get()
    if existing.exists:
        current_qty = existing.to_dict().get("quantity",0)
        cart_item_ref.update({ "quantity": current_qty + quantity})
        print(f" Updated {product_data["name"]} in cart to {current_qty + quantity} items.")

    else:
        cart_item_ref.set({
            "name": product_data["name"],
            "price": product_data["price"],
            "quantity": quantity
        })
        print(f" Added {product_data["name"]} to cart.")

def view_cart(user_id):
    cart_ref = db.collection("users").document(user_id).collection("cart")
    cart_items = cart_ref.stream()
    total = 0
    found = False

    print("\n🛒 Your Cart:")
    for item in cart_items:
        found = True
        data   = item.to_dict()
        subtotal = data["quantity"] * data["price"]
        total += subtotal
        print(f"- {data["name"]} (x{data["quantity"]}) - ${data["price"]} each | Subtotal: ${subtotal:.2f}")

    if found:
        print(f"Total: ${total:.2f}\n")
    else:
        print("Cart is empty.\n")

def place_order_from_cart(user_id):
    cart_ref = db.collection("users").document(user_id).collection("cart")
    cart_items =  list(cart_ref.stream())

    if not cart_items:
        print("❌ Your cart 🛒 is empty. Add items to your cart before placing an order.")
        return
    order_items = []
    total = 0
    for item in cart_items:
        data = item.to_dict()
        order_items.append({
            "product_id": item.id,
            "name": data["name"],
            "quantity": data["quantity"],
            "price": data["price"] 
        })
        total += data["quantity"] * data["price"]
    order_data = {
        "user_id": user_id,
        "items": order_items,
        "total_price": total,
        "order_date": datetime.utcnow().isoformat()

    }

    db.collection("orders").add(order_data)
    print(f"✅ Order placed successfully! Total: ${total:.2f}")
    # Clear the cart after placing the order
    for item in cart_items:
        item.reference.delete()


def clear_cart(user_id):
    cart_ref= db.collection("users").document(user_id).collection("cart")
    cart_items = list(cart_ref.stream())
    for item in cart_items:
        item.reference.delete()

    print("\n🗑️ Cart cleared successfully.")
 
        

FIREBASE_API_KEY = "AIzaSyAtuUjvCtOVX1q3zKUEVsParWWR9TXjIZo"

FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

def signup_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code == 200:
            print("✅ User registered successfully.")
            return data
        else:
            error_message = data.get("error", {}).get("message", "UNKNOWN_ERROR")

            friendly_errors = {
                "EMAIL_EXISTS": "❌ This email is already registered.",
                "INVALID_EMAIL": "❌ Please enter a valid email address.",
                "WEAK_PASSWORD": "❌ Password should be at least 6 characters.",
            }

            # Input Error Handling"
            for key in friendly_errors:
                if key in error_message:
                    print(friendly_errors[key])
                    break
            else:
                print(f"⚠️ Registration failed: {error_message}")

            return None

    except requests.exceptions.RequestException as e:
        print("🔥 Network error during registration:", e)
        return None

def login_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code == 200:
            print("✅ Login successful.")
            return data
        else:
            error_message = data.get("error", {}).get("message", "UNKNOWN_ERROR")

            friendly_errors = {
                "EMAIL_NOT_FOUND": "❌ Email not found. Try again or sign up.",
                "INVALID_PASSWORD": "❌ Incorrect password. Please try again.",
                "USER_DISABLED": "🚫 This user account has been disabled.",
                "INVALID_LOGIN_CREDENTIALS": "❌ Invalid email or password."
            }

            print(friendly_errors.get(error_message, f"⚠️ Login failed: {error_message}"))
            return None

    except requests.exceptions.RequestException as e:
        print("🔥 Network error:", e)
        return None