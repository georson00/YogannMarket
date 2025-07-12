from firestore_service import *

logged_in_user = None

def menu():
    global logged_in_user
    while True:
        print("\n==== E-Commerce Cloud App ====")
        print("1. Add user (Seller)")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. View All Products")
        print("6. View Products by User (Seller) ID")
        print("7. Add to Cart")
        print("8. View Cart")
        print("9. Clear Cart")
        print("10. Place Order from Cart")
        print("11. View Orders by User")
        print("12. Sign Up (Create Account)")
        print("13. Log In")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_user(
                input("User ID: "),
                input("Name: "),
                input("Email: ")
            )
        elif choice == "2":
            add_product(
                input("Product ID: "),
                input("Product Name: "),
                float(input("Price: ")),
                input("Description: "),
                input("User ID (Seller): ")
            )
        elif choice == "3":
            pid = input("Product ID to update: ")
            field = input("Field to update (name, price, description): ")
            value = input("New value: ")
            update_product(pid, {field: float(value) if field == "price" else value})
            print("✅Product updated successfully.")
        elif choice == "4":
            delete_product(input("Product ID to delete: "))
        elif choice == "5":
            get_all_products()
        elif choice == "6":
            get_products_by_user(input("User ID: "))
        
        elif choice == "7":
            if not logged_in_user:
                print("You must be logged in to add items to cart.")
                continue

            user_id = logged_in_user["user_id"]
            product_id = input("Product ID: ")
            quantity = int(input("Quantity: "))
            add_to_cart(user_id, product_id, quantity)
        elif choice == "8":
            if not logged_in_user:
                print("You must be logged in to view your cart.")
                continue
            
            user_id = logged_in_user["user_id"]
            view_cart(user_id)
        elif choice == "9":
            if not logged_in_user:
                print("You must be logged in to clear your cart.")
                continue
            
            user_id = logged_in_user["user_id"]
            clear_cart(user_id)

        elif choice == "10":
            if not logged_in_user:
                print("You must be logged in to place an order.")
                continue
            
            user_id = logged_in_user["user_id"]
            place_order_from_cart(user_id)

        elif choice == "11":
            user_id = input("User ID: ")
            get_orders_by_user(user_id)

        elif choice == "12":
            print("Create a new account.")
            full_name = input("Full Name: ")
            email = input("Email: ")
            password = input("Password: ")
            signup_user(full_name, email, password)

        elif choice == "13":
            email = input("Email: ")
            password = input("Password: ")
            user_data = login_user(email, password)
            if user_data:
                print("Login successful.")
                logged_in_user = {
                    "email": email,
                    "user_id": user_data["localId"],
                    "id_token": user_data["idToken"]
                }

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()