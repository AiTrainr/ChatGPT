import tkinter as tk
from tkinter import ttk
import csv

# Global variables
inventory_file = 'inventory.csv'
inventory = []
changes_made = False  # Added this variable to track if changes were made to the inventory data

# Load the inventory data from file
def load_inventory():
    global inventory
    try:
        with open(inventory_file, 'r') as f:
            reader = csv.reader(f)
            inventory = list(reader)
    except FileNotFoundError:
        inventory = []

# Save the inventory data to file
def save_inventory(inventory):
    with open(inventory_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(inventory)

# Add or adjust the quantity for a component
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
    # Update the inventory table and save the inventory data to file if changes were made
    update_inventory_table()
    global changes_made
    changes_made = True

# Update the inventory table
def update_inventory_table():
    # Clear any existing rows
    for row in inventory_table.get_children():
        inventory_table.delete(row)
    # Add rows from inventory data
    for item in inventory:
        inventory_table.insert('', 'end', values=item)
    # Save the inventory data to file if changes were made
    global changes_made
    if changes_made:
        save_inventory(inventory)
        changes_made = False

# Handle the "Add or Adjust Qty" button click
def input_qty():
    # Define the Input popup window
    input_popup = tk.Toplevel(root)
    input_popup.title('Add or Adjust Qty')
    input_popup.geometry('300x100')

    # Define the name and qty entry fields and labels
    name_label = ttk.Label(input_popup, text='Component Name')
    name_label.grid(row=0, column=0)
    name_entry = ttk.Entry(input_popup)
    name_entry.grid(row=0, column=1)
    qty_label = ttk.Label(input_popup, text='Qty (+ or -)')
    qty_label.grid(row=1, column=0)
    qty_entry = ttk.Entry(input_popup)
    qty_entry.grid(row=1, column=1)

    # Define the Change button and its command
    def change_qty_command():
        name = name_entry.get()
        qty = qty_entry.get()
        if name != '' and qty != '':
            change_qty(name, qty)
            input_popup.destroy()

    change_button = ttk.Button(input_popup, text='Change
    change_button.config(command=change_qty_command)
    change_button.grid(row=2, column=0, columnspan=2)
    name_entry.focus()  # Focus the cursor on the name entry field

# Define the main window
root = tk.Tk()
root.title('Inventory Organizer')

# Define the notebook widget and its tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Define the Inventory tab and its table
inventory_tab = ttk.Frame(notebook)
inventory_tab.pack(fill='both', expand=True)
notebook.add(inventory_tab, text='Inventory')

inventory_table = ttk.Treeview(inventory_tab, columns=('Location', 'Name', 'Qty'))
inventory_table.heading('#0', text='')
inventory_table.heading('Location', text='Location')
inventory_table.heading('Name', text='Name')
inventory_table.heading('Qty', text='Qty')
inventory_table.column('#0', width=0, stretch='no')
inventory_table.column('Location', anchor='center', width=100)
inventory_table.column('Name', anchor='w', width=200)
inventory_table.column('Qty', anchor='center', width=100)
inventory_table.pack(fill='both', expand=True)

# Define the Add or Adjust Qty button
add_qty_button = ttk.Button(root, text='Add or Adjust Qty', command=input_qty)
add_qty_button.pack(side='bottom')

# Load the inventory data and update the inventory table
load_inventory()
update_inventory_table()

root.mainloop()
