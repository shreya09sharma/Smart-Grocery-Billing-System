# SMART GROCERY BILLING SYSTEM (FINAL ADVANCED VERSION)
# Added: Customer Login, Festive Offers, Product Search + ID

import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ================= DATABASE =================
client = MongoClient("mongodb://localhost:27017/")
db = client["grocery_store"]
products_col = db["products"]
sales_col = db["sales"]

# ================= SAMPLE PRODUCTS =================
def insert_products():
    if products_col.count_documents({}) == 0:
        products_col.insert_many([
            {"id": 1, "name": "Rice", "price": 50},
            {"id": 2, "name": "Milk", "price": 30},
            {"id": 3, "name": "Sugar", "price": 45},
            {"id": 4, "name": "Oil", "price": 120},
        ])
insert_products()

# ================= GLOBAL VARIABLES =================
bill = []
customer_name = ""
customer_phone = ""

# ================= FESTIVE OFFER =================
def apply_offer(amount):
    if amount > 500:
        return amount * 0.10
    return 0

# ================= GST =================
def gst_calc(amount):
    return np.multiply(amount, 0.05)

# ================= LOGIN =================
def login():
    global customer_name, customer_phone
    customer_name = name_entry.get()
    customer_phone = phone_entry.get()

    if customer_name == "" or customer_phone == "":
        messagebox.showerror("Error", "Enter details")
    else:
        login_window.destroy()
        main_window()

# ================= SEARCH PRODUCT =================
def search_product():
    name = search_entry.get().lower()
    results = products_col.find({})

    listbox.delete(0, tk.END)

    for p in results:
        if name in p['name'].lower():
            listbox.insert(tk.END, f"ID:{p['id']} | {p['name']} | ₹{p['price']}")

# ================= ADD ITEM =================
def add_item():
    try:
        pid = id_entry.get()
        pname = name_entry2.get().lower()
        qty = int(qty_entry.get())

        product = None

        # Search by ID
        if pid != "":
            product = products_col.find_one({"id": int(pid)})

        # Search by Name
        elif pname != "":
            product = products_col.find_one({"name": {"$regex": pname, "$options": "i"}})

        if product:
            total = product['price'] * qty
            bill.append({
                "name": product['name'],
                "qty": qty,
                "price": product['price'],
                "total": total
            })

            listbox.insert(tk.END, f"Added: {product['name']} x {qty} = ₹{total}")
        else:
            messagebox.showerror("Error", "Product not found")
    except:
        messagebox.showerror("Error", "Invalid Input")

# ================= BILL =================
def generate_bill():
    if not bill:
        messagebox.showwarning("Empty", "No items")
        return

    subtotal = sum(item['total'] for item in bill)
    discount = apply_offer(subtotal)
    after_discount = subtotal - discount
    gst = gst_calc(after_discount)
    final = after_discount + gst

    text.delete(1.0, tk.END)

    text.insert(tk.END, "===== SUVIDHA STORE BILL =====\n")
    text.insert(tk.END, f"Customer: {customer_name}\nPhone: {customer_phone}\n\n")

    for item in bill:
        text.insert(tk.END, f"{item['name']} x {item['qty']} = ₹{item['total']}\n")

    text.insert(tk.END, f"\nSubtotal: ₹{subtotal}")
    text.insert(tk.END, f"\nDiscount: -₹{discount}")
    text.insert(tk.END, f"\nGST: ₹{gst}")
    text.insert(tk.END, f"\nFinal Amount: ₹{final}")

    sales_col.insert_one({
        "customer": customer_name,
        "phone": customer_phone,
        "total": float(final),
        "date": datetime.now()
    })

# ================= SAVE =================
def save_bill():
    content = text.get(1.0, tk.END)
    name = f"bill_{datetime.now().strftime('%H%M%S')}.txt"
    with open(name, "w") as f:
        f.write(content)
    messagebox.showinfo("Saved", "Bill Saved")

# ================= REPORT =================
def report():
    data = list(sales_col.find())
    if not data:
        messagebox.showwarning("No Data", "No sales")
        return

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date

    result = df.groupby('day')['total'].sum()
    messagebox.showinfo("Report", str(result))

# ================= GRAPH =================
def graph():
    data = list(sales_col.find())
    if not data:
        return

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date

    result = df.groupby('day')['total'].sum()

    plt.figure()
    result.plot()
    plt.title("Sales Graph")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.show()

# ================= MAIN WINDOW =================
def main_window():
    global id_entry, name_entry2, qty_entry, listbox, text, search_entry

    root = tk.Tk()
    root.title("Suvidha Grocery System")

    tk.Label(root, text="Search Product").pack()
    search_entry = tk.Entry(root)
    search_entry.pack()
    tk.Button(root, text="Search", command=search_product).pack()

    tk.Label(root, text="Product ID").pack()
    id_entry = tk.Entry(root)
    id_entry.pack()

    tk.Label(root, text="OR Product Name").pack()
    name_entry2 = tk.Entry(root)
    name_entry2.pack()

    tk.Label(root, text="Quantity").pack()
    qty_entry = tk.Entry(root)
    qty_entry.pack()

    tk.Button(root, text="Add Item", command=add_item).pack()
    tk.Button(root, text="Generate Bill", command=generate_bill).pack()
    tk.Button(root, text="Save Bill", command=save_bill).pack()
    tk.Button(root, text="Report", command=report).pack()
    tk.Button(root, text="Graph", command=graph).pack()

    listbox = tk.Listbox(root)
    listbox.pack(fill=tk.BOTH, expand=True)

    text = tk.Text(root, height=10)
    text.pack()

    root.mainloop()

# ================= LOGIN WINDOW =================
login_window = tk.Tk()
login_window.title("Customer Login")

tk.Label(login_window, text="Enter Name").pack()
name_entry = tk.Entry(login_window)
name_entry.pack()

tk.Label(login_window, text="Enter Phone Number").pack()
phone_entry = tk.Entry(login_window)
phone_entry.pack()

tk.Button(login_window, text="Start Shopping", command=login).pack()

login_window.mainloop()
