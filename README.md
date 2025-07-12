
# Overview

This project is a command-line E-Commerce system designed to deepen my experience with cloud-integrated applications as I work toward becoming a professional software developer. The goal was to explore how cloud databases can be used to manage users, products, and orders in a dynamic and secure environment.

The software allows users to register and log in securely using Firebase Authentication. Authenticated users can browse products, place orders with multiple items, and view order history. All user, product, and order data is stored and managed in a Firestore cloud database. This simulates a real-world backend system for an online shopping experience.

The purpose of writing this software is to strengthen my understanding of cloud database interaction using Python, and to practice developing scalable, secure backend logic. It helped me better understand data relationships, authentication workflows, and cloud integration best practices.

[Software Demo Video](https://youtu.be/VtP1qBdO6Sk)

---

# Cloud Database

I used **Google Firebase Firestore** as the cloud database service. Firestore is a NoSQL document database that offers real-time data syncing and cloud hosting, which made it ideal for managing e-commerce data.

### Database Structure:
- `users`: Stores registered user accounts with fields like `name`, `email`, and `created_at`.
- `products`: Stores products available for purchase. Each product includes `name`, `price`, `description`, `user_id` (who created it), and `created_at`.
- `orders`: Stores customer orders. Each order includes:
  - `user_id`
  - `items`: a list of products with `product_id`, `product_name`, `price`, `quantity`, and `subtotal`
  - `total_price`
  - `order_date`

This structure allows for relationships between collections and simulates a real-world e-commerce system.

---
## 🛑 Security
- **Do not commit `serviceAccountKey.json` to public repositories.**
# Development Environment

- **Operating System**: Windows 10
- **Code Editor**: Visual Studio Code
- **Cloud Platform**: Firebase (Firestore + Authentication)

### Programming Language & Libraries:
- Python 3.13
- `firebase-admin`: for accessing Firestore
- `requests`: for interacting with Firebase Authentication REST API
- `datetime`: for timestamping data

---

# Useful Websites

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup)
- [Firestore Python Client Docs](https://googleapis.dev/python/firestore/latest/index.html)
- [Python Official Documentation](https://docs.python.org/3/)
- [Stack Overflow](https://stackoverflow.com/)

---

# Future Work

- Add real-time notifications for product or order changes
- Build a web interface using Flask or Streamlit
- Allow users to update or cancel their own orders
- Add roles: admin vs customer (with permissions)
- Store and retrieve product images
- Improve password strength feedback and validation
