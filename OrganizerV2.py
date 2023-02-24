import tkinter as tk
from tkinter import ttk
import csv

# Function to load inventory data from file
def load_inventory():
    inventory = []
    with open('inventory.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            inventory.append(row)
    return inventory

# Function to save inventory data to file
def save_inventory(inventory):
    with open('inventory.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(inventory)

# Function to update the inventory table
def update_inventory_table():
    # Clear any existing rows
    for row in inventory_table.get_children():
        inventory_table.delete(row)
    # Add rows from inventory data
    for item in inventory:
        inventory_table.insert('', 'end', values=item)

# Function to handle the "Add or Adjust Qty" button click
def add_or_adjust_qty():
    # Create the Input popup window
    input_window = tk.Toplevel(root)
    input_window.title("Input")
    # Add widgets to the Input window
    name_label = tk.Label(input_window, text="Component Name:")
    name_label.pack()
    name_entry = tk.Entry(input_window)
    name_entry.pack()
    qty_label = tk.Label(input_window, text="Change in Quantity:")
    qty_label.pack()
    qty_entry = tk.Entry(input_window)
    qty_entry.pack()
    change_button = tk.Button(input_window, text="Change", command=lambda: change_qty(name_entry.get(), qty_entry.get()))
    change_button.pack()

# Function to handle the "Change" button click
def change_qty(name, qty):
    global inventory
    # Find the row for the component in the inventory data
    index = -1
    for i, item in enumerate(inventory):
        if item[1] == name:
            index = i
            break
    # If the component is not found, add a new row to the inventory data
    if index == -1:
        inventory.append(['', name, 0])
        index = len(inventory) - 1
    # Update the quantity for the component
    inventory[index][2] = str(int(inventory[index][2]) + int(qty))
    # Update the inventory table and save the inventory data to file
    update_inventory_table()
    save_inventory(inventory)

# Load inventory data from file
inventory = load_inventory()

# Create the main window
root = tk.Tk()
root.title("Inventory Management")

# Create the tabs
notebook = ttk.Notebook(root)
inventory_tab = ttk.Frame(notebook)
notebook.add(inventory_tab, text="Inventory")

# Create the inventory table
inventory_table = ttk.Treeview(inventory_tab, columns=('location', 'name', 'qty'), show='headings')
inventory_table.heading('location', text='Location')
inventory_table.heading('name', text='Name')
inventory_table.heading('qty', text='Qty')
inventory_table.pack(side='left')

# Add the "Add or Adjust Qty" button to the main window
add_or_adjust_button = tk.Button(root, text="Add or Adjust Qty", command=add_or_adjust_qty)
add_or_adjust_button.pack(side='bottom')

# Populate the inventory table with data
update_inventory_table()

# Start the main loop
root.mainloop()
