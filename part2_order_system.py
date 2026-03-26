# =========================================================
# Part 2: Data Structures
# Theme: Restaurant Menu & Order Management System
# =========================================================

import copy

# ---------------------------------------------------------
# Provided Data (copied exactly as given)
# ---------------------------------------------------------

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}

# =========================================================
# Task 1 — Explore the Menu
# =========================================================

print("\n" + "=" * 60)
print("TASK 1 — EXPLORE THE MENU")
print("=" * 60)

# Loop through categories first, then filter items by category
categories = ["Starters", "Mains", "Desserts"]

for category in categories:
    print(f"\n===== {category} =====")
    for item_name, details in menu.items():
        if details["category"] == category:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item_name:15} ₹{details['price']:7.2f}   [{status}]")

# Total number of items on menu
total_menu_items = len(menu)

# Total number of available items
total_available_items = sum(1 for details in menu.values() if details["available"])

# Most expensive item
most_expensive_item = max(menu.items(), key=lambda item: item[1]["price"])
most_expensive_name = most_expensive_item[0]
most_expensive_price = most_expensive_item[1]["price"]

# Items under ₹150
items_under_150 = []
for item_name, details in menu.items():
    if details["price"] < 150:
        items_under_150.append((item_name, details["price"]))

print("\n----- Menu Statistics -----")
print(f"Total number of items      : {total_menu_items}")
print(f"Total available items      : {total_available_items}")
print(f"Most expensive item        : {most_expensive_name} (₹{most_expensive_price:.2f})")

print("\nItems priced under ₹150:")
for item_name, price in items_under_150:
    print(f"- {item_name} (₹{price:.2f})")

# =========================================================
# Task 2 — Cart Operations
# =========================================================

print("\n" + "=" * 60)
print("TASK 2 — CART OPERATIONS")
print("=" * 60)

cart = []

def print_cart(cart_data, heading="Current Cart"):
    """Print the current cart state."""
    print(f"\n--- {heading} ---")
    if not cart_data:
        print("Cart is empty.")
        return

    for entry in cart_data:
        item_total = entry["quantity"] * entry["price"]
        print(f"{entry['item']:15} x{entry['quantity']}   ₹{item_total:.2f}")

def add_to_cart(cart_data, item_name, quantity):
    """Add item to cart after checking menu and availability."""
    if item_name not in menu:
        print(f"Cannot add '{item_name}' — item does not exist in menu.")
        return

    if not menu[item_name]["available"]:
        print(f"Cannot add '{item_name}' — item is currently unavailable.")
        return

    for entry in cart_data:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            print(f"Updated '{item_name}' quantity to {entry['quantity']}.")
            return

    cart_data.append({
        "item": item_name,
        "quantity": quantity,
        "price": menu[item_name]["price"]
    })
    print(f"Added '{item_name}' x{quantity} to cart.")

def remove_from_cart(cart_data, item_name):
    """Remove an item from the cart by name."""
    for entry in cart_data:
        if entry["item"] == item_name:
            cart_data.remove(entry)
            print(f"Removed '{item_name}' from cart.")
            return
    print(f"Cannot remove '{item_name}' — item not found in cart.")

def update_quantity(cart_data, item_name, new_quantity):
    """Update quantity of an item already in the cart."""
    for entry in cart_data:
        if entry["item"] == item_name:
            entry["quantity"] = new_quantity
            print(f"Updated '{item_name}' quantity to {new_quantity}.")
            return
    print(f"Cannot update '{item_name}' — item not found in cart.")

# Simulate the required sequence
add_to_cart(cart, "Paneer Tikka", 2)
print_cart(cart, "After adding Paneer Tikka x2")

add_to_cart(cart, "Gulab Jamun", 1)
print_cart(cart, "After adding Gulab Jamun x1")

add_to_cart(cart, "Paneer Tikka", 1)
print_cart(cart, "After adding Paneer Tikka x1 again")

add_to_cart(cart, "Mystery Burger", 1)
print_cart(cart, "After trying to add Mystery Burger")

add_to_cart(cart, "Chicken Wings", 1)
print_cart(cart, "After trying to add Chicken Wings")

remove_from_cart(cart, "Gulab Jamun")
print_cart(cart, "After removing Gulab Jamun")

# Final order summary
print("\n========== Order Summary ==========")
subtotal = 0

for entry in cart:
    item_total = entry["quantity"] * entry["price"]
    subtotal += item_total
    print(f"{entry['item']:18} x{entry['quantity']:<3} ₹{item_total:.2f}")

gst = subtotal * 0.05
total_payable = subtotal + gst

print("-" * 36)
print(f"{'Subtotal:':25} ₹{subtotal:.2f}")
print(f"{'GST (5%):':25} ₹{gst:.2f}")
print(f"{'Total Payable:':25} ₹{total_payable:.2f}")
print("=" * 36)

# =========================================================
# Task 3 — Inventory Tracker with Deep Copy
# =========================================================

print("\n" + "=" * 60)
print("TASK 3 — INVENTORY TRACKER WITH DEEP COPY")
print("=" * 60)

# Deep copy inventory before making changes
inventory_backup = copy.deepcopy(inventory)

# Demonstrate that deep copy works
print("\nDemonstrating deep copy:")
print(f"Original stock of Paneer Tikka in inventory       : {inventory['Paneer Tikka']['stock']}")
print(f"Original stock of Paneer Tikka in inventory_backup: {inventory_backup['Paneer Tikka']['stock']}")

# Manually change one stock value in inventory
inventory["Paneer Tikka"]["stock"] = 99

print("\nAfter manually changing inventory['Paneer Tikka']['stock'] to 99:")
print(f"inventory['Paneer Tikka']['stock']       = {inventory['Paneer Tikka']['stock']}")
print(f"inventory_backup['Paneer Tikka']['stock'] = {inventory_backup['Paneer Tikka']['stock']}")

# Restore inventory to original state before continuing
inventory = copy.deepcopy(inventory_backup)

print("\nInventory restored before continuing.")
print(f"Restored inventory stock of Paneer Tikka: {inventory['Paneer Tikka']['stock']}")

# Deduct quantities from final cart
print("\nFulfilling final cart order:")
for entry in cart:
    item_name = entry["item"]
    qty_needed = entry["quantity"]

    if item_name in inventory:
        current_stock = inventory[item_name]["stock"]

        if current_stock >= qty_needed:
            inventory[item_name]["stock"] -= qty_needed
            print(f"{item_name}: Deducted {qty_needed} unit(s). Remaining stock = {inventory[item_name]['stock']}")
        else:
            print(f"Warning: Insufficient stock for {item_name}. Only {current_stock} unit(s) available.")
            inventory[item_name]["stock"] = 0
            print(f"{item_name}: Deducted only {current_stock} unit(s). Remaining stock = 0")

# Reorder alerts
print("\nReorder Alerts:")
alert_found = False
for item_name, details in inventory.items():
    if details["stock"] <= details["reorder_level"]:
        alert_found = True
        print(f"⚠ Reorder Alert: {item_name} — Only {details['stock']} unit(s) left (reorder level: {details['reorder_level']})")

if not alert_found:
    print("No reorder alerts at the moment.")

# Print both inventory and backup to confirm they differ
print("\nCurrent Inventory After Fulfilment:")
for item_name, details in inventory.items():
    print(f"{item_name:15} Stock: {details['stock']}, Reorder Level: {details['reorder_level']}")

print("\nInventory Backup (Original Copy):")
for item_name, details in inventory_backup.items():
    print(f"{item_name:15} Stock: {details['stock']}, Reorder Level: {details['reorder_level']}")

# =========================================================
# Task 4 — Daily Sales Log Analysis
# =========================================================

print("\n" + "=" * 60)
print("TASK 4 — DAILY SALES LOG ANALYSIS")
print("=" * 60)

def compute_daily_revenue(log_data):
    """Return a dictionary of total revenue per day."""
    revenue_per_day = {}
    for date, orders in log_data.items():
        daily_total = 0
        for order in orders:
            daily_total += order["total"]
        revenue_per_day[date] = daily_total
    return revenue_per_day

def print_revenue_table(log_data):
    """Print revenue per day and best-selling day."""
    revenue_per_day = compute_daily_revenue(log_data)

    print("\nRevenue Per Day:")
    for date, revenue in revenue_per_day.items():
        print(f"{date} : ₹{revenue:.2f}")

    best_day = max(revenue_per_day, key=revenue_per_day.get)
    print(f"\nBest-selling day: {best_day} (₹{revenue_per_day[best_day]:.2f})")

# Initial revenue per day
print_revenue_table(sales_log)

# Find the most ordered item
item_order_count = {}

for date, orders in sales_log.items():
    for order in orders:
        for item_name in order["items"]:
            if item_name in item_order_count:
                item_order_count[item_name] += 1
            else:
                item_order_count[item_name] = 1

most_ordered_item = max(item_order_count, key=item_order_count.get)
print(f"\nMost ordered item: {most_ordered_item} ({item_order_count[most_ordered_item]} orders)")

# Add new day to sales_log
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]

print("\nAfter adding sales for 2025-01-05:")
print_revenue_table(sales_log)

# Print numbered list of all orders across all dates
print("\nNumbered List of All Orders:")
all_orders = []

for date, orders in sales_log.items():
    for order in orders:
        all_orders.append((date, order))

for index, (date, order) in enumerate(all_orders, start=1):
    items_text = ", ".join(order["items"])
    print(f"{index}. [{date}] Order #{order['order_id']} — ₹{order['total']:.2f} — Items: {items_text}")
