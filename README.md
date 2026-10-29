# 🛒 Smart Grocery Billing System

## 📌 About the Project
The Smart Grocery Billing System is a Python-based application developed to simplify grocery shopping and billing. It provides a graphical user interface using Tkinter and stores product and sales information in MongoDB.

## ✨ Features
- Customer Login
- Product Search by Name
- Add Products using Product ID or Name
- Automatic Bill Generation
- GST Calculation (5%)
- Festive Discount (10% on purchases above ₹500)
- Save Bills as Text Files
- Daily Sales Reports
- Graphical Sales Analysis

## 🛠️ Technologies Used
- Python
- Tkinter
- MongoDB
- PyMongo
- Pandas
- NumPy
- Matplotlib

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
```

### 2. Install Required Libraries
```bash
pip install pymongo pandas numpy matplotlib
```

### 3. Start MongoDB
Ensure that MongoDB is installed and running on your system.

### 4. Run the Application
```bash
python smart_grocery_billing_system.py
```

## 🧾 How It Works
1. Enter your name and phone number.
2. Search for grocery products.
3. Enter the product ID or name and quantity.
4. Add items to the bill.
5. Generate the bill to calculate the subtotal, discount, GST, and final amount.
6. Save the bill as a text file.
7. View sales reports and graphs.

## 🗄️ Database
The application uses MongoDB with the following database and collections:
- **Database:** `grocery_store`
- **Products Collection:** `products`
- **Sales Collection:** `sales`

## 👩‍💻 Author
**Shreya Sharma**

---
⭐ If you find this project useful, feel free to explore and improve it!
