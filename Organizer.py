import tkinter as tk
from datetime import datetime
import os
import json

data = {}
revision_log = []

# Check if the JSON file exists, and if so, load the data
if os.path.exists('component_data.json'):
    with open('component_data.json', 'r') as f:
        data = json.load(f)

# Check if the revision log file exists, and if so, load the data
if os.path.exists('revision_log.json'):
    with open('revision_log.json', 'r') as f:
        revision_log = json.load(f)

def save_data():
    # Save the data to a JSON file
    with open('component_data.json', 'w') as f:
        json.dump(data, f)
    
    # Save the revision log to a JSON file
    with open('revision_log.json', 'w') as f:
        json.dump(revision_log, f)

def update_component(name, quantity_change):
    global data
    global revision_log
    
    # Update the quantity of the specified component
    if name in data:
        data[name] += quantity_change
    else:
        data[name] = quantity_change
    
    # Log the revision
    revision_log.append({
        'name': name,
        'prev_quantity': data[name] - quantity_change,
        'change': quantity_change,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

def display_data():
    # Create a new window to display the component data
    window = tk.Toplevel()
    window.title('Component Data')
    
    # Create a table to display the component data
    table = tk.Frame(window)
    
    # Create the headers for the table
    name_header = tk.Label(table, text='Name', font=('Arial', 12, 'bold'))
    name_header.grid(row=0, column=0, padx=5, pady=5)
    
    quantity_header = tk.Label(table, text='Quantity', font=('Arial', 12, 'bold'))
    quantity_header.grid(row=0, column=1, padx=5, pady=5)
    
    # Add the component data to the table
    row = 1
    for name, quantity in data.items():
        name_label = tk.Label(table, text=name, font=('Arial', 12))
        name_label.grid(row=row, column=0, padx=5, pady=5)
        
        quantity_label = tk.Label(table, text=quantity, font=('Arial', 12))
        quantity_label.grid(row=row, column=1, padx=5, pady=5)
        
        row += 1
    
    table.pack()

def update_quantity():
    # Create a new window to update the quantity of a component
    window = tk.Toplevel()
    window.title('Update Quantity')
    
    # Create a dropdown menu to select the component
    component_var = tk.StringVar(window)
    component_var.set(next(iter(data)))
    
    component_menu = tk.OptionMenu(window, component_var, *data.keys())
    component_menu.pack(padx=5, pady=5)
    
    # Create a text entry for the quantity change
    quantity_label = tk.Label(window, text='Quantity Change:', font=('Arial', 12))
    quantity_label.pack(padx=5, pady=5)
    
    quantity_entry = tk.Entry(window, font=('Arial', 12))
    quantity_entry.pack(padx=5, pady=5)
    
    # Create a button to update the quantity
    def update():
        try:
            quantity_change = int(quantity_entry.get())
            name = component_var