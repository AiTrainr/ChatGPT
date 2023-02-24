import tkinter as tk
import csv

# Define the inventory file name
INVENTORY_FILE = "inventory.csv"

# Define the inventory headers
INVENTORY_HEADERS = ["Location", "Name", "Qty"]

# Define the default inventory data
DEFAULT_INVENTORY = [
    ["Shelf 1", "Arduino Uno", 10],
    ["Shelf 2", "Breadboard", 20],
    ["Shelf 3", "Jumper wires", 100],
    ["Shelf 4", "Resistors", 50],
    ["Shelf 5", "LEDs", 30]
]

# Create a dictionary to hold the inventory data
inventory_data = {}

def read_inventory():
    """Read the inventory data from the CSV file"""
    try:
        with open(INVENTORY_FILE, newline="") as inventory_file:
            inventory_reader = csv.reader(inventory_file)
            # Skip the header row
            next(inventory_reader)
            # Read each row and store it in the inventory dictionary
            for row in inventory_reader:
                location, name, qty = row
                inventory_data[name] = {"Location": location, "Qty": int(qty)}
    except FileNotFoundError:
        # If the file is not found, use the default inventory data
        for row in DEFAULT_INVENTORY:
            location, name, qty = row
            inventory_data[name] = {"Location": location, "Qty": qty}

def write_inventory():
    """Write the inventory data to the CSV file"""
    with open(INVENTORY_FILE, "w", newline="") as inventory_file:
        inventory_writer = csv.writer(inventory_file)
        inventory_writer.writerow(INVENTORY_HEADERS)
        for name, data in inventory_data.items():
            location = data["Location"]
            qty = data["Qty"]
            inventory_writer.writerow([location, name, qty])

def input_popup(root, inventory):
    """Display the input popup window"""
    def change_qty():
        """Update the quantity for the selected component"""
        name = name_var.get()
        location = location_var.get()
        qty_change = int(qty_var.get())
        # If the component already exists in the inventory, update its quantity
        if name in inventory_data:
            inventory_data[name]["Qty"] += qty_change
            inventory_data[name]["Location"] = location
        # Otherwise, add the component to the inventory
        else:
            inventory_data[name] = {"Location": location, "Qty": qty_change}
        write_inventory()
        update_inventory_table(inventory)

    input_window = tk.Toplevel(root)

    name_label = tk.Label(input_window, text="Name:")
    name_var = tk.StringVar()
    name_entry = tk.Entry(input_window, textvariable=name_var)

    location_label = tk.Label(input_window, text="Location:")
    location_var = tk.StringVar()
    location_entry = tk.Entry(input_window, textvariable=location_var)

    qty_label = tk.Label(input_window, text="Qty:")
    qty_var = tk.StringVar()
    qty_entry = tk.Entry(input_window, textvariable=qty_var)

    change_button = tk.Button(input_window, text="Change", command=change_qty)

    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    location_label.grid(row=1, column=0, padx=5, pady=5)
    location_entry.grid(row=1, column=1, padx=5, pady=5)

    qty_label.grid(row=2, column=0, padx=5, pady=5)
    qty_entry.grid(row=2, column=1, padx=5, pady=5)
    
    name_label = tk.Label(input_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = tk.Entry(input_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    location_label = tk.Label(input_frame, text="Location:")
    location_label.grid(row=1, column=0, padx=5, pady=5)

    location_entry = tk.Entry(input_frame)
    location_entry.grid(row=1, column=1, padx=5, pady=5)

    qty_label = tk.Label(input_frame, text="Change in Qty:")
    qty_label.grid(row=2, column=0, padx=5, pady=5)

    qty_entry = tk.Entry(input_frame)
    qty_entry.grid(row=2, column=1, padx=5, pady=5)

    change_button = tk.Button(input_frame, text="Change", command=change_qty)
    change_button.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
