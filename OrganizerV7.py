import tkinter as tk
import csv

inventory_file_path = 'inventory.csv'

root = tk.Tk()

def read_inventory():
    """Reads the inventory from the CSV file."""
    try:
        with open(inventory_file_path, 'r') as file:
            reader = csv.reader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def write_inventory():
    """Writes the inventory to the CSV file."""
    with open(inventory_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Location', 'Name', 'Qty'])
        writer.writerows(inventory)

def update_inventory_table():
    """Updates the Inventory tab with the current inventory."""
    # Clear the current contents of the inventory table
    for widget in inventory_frame.winfo_children():
        widget.destroy()

    # Create the header row of the inventory table
    location_label = tk.Label(inventory_frame, text='Location')
    location_label.grid(row=0, column=0, padx=5, pady=5)
    name_label = tk.Label(inventory_frame, text='Name')
    name_label.grid(row=0, column=1, padx=5, pady=5)
    qty_label = tk.Label(inventory_frame, text='Qty')
    qty_label.grid(row=0, column=2, padx=5, pady=5)

    # Add each component in the inventory to the table
    for i, row in enumerate(inventory):
        location = tk.Label(inventory_frame, text=row[0])
        location.grid(row=i+1, column=0, padx=5, pady=5)
        name = tk.Label(inventory_frame, text=row[1])
        name.grid(row=i+1, column=1, padx=5, pady=5)
        qty = tk.Label(inventory_frame, text=row[2])
        qty.grid(row=i+1, column=2, padx=5, pady=5)

def add_or_adjust_qty():
    """Displays the Input popup to add or adjust a component quantity."""
    # Create the Input popup
    input_popup = tk.Toplevel(root)
    input_popup.title('Add or Adjust Qty')

    # Create the name label and entry field
    name_label = tk.Label(input_popup, text='Name:')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(input_popup)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create the location label and entry field
    location_label = tk.Label(input_popup, text='Location:')
    location_label.grid(row=1, column=0, padx=5, pady=5)
    location_entry = tk.Entry(input_popup)
    location_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create the qty label and entry field
    qty_label = tk.Label(input_popup, text='Qty:')
    qty_label.grid(row=2, column=0, padx=5, pady=5)
    qty_entry = tk.Entry(input_popup)
    qty_entry.grid(row=2, column=1, padx=5, pady=5)

    def submit_qty():
        """Submits the entered quantity."""
        name = name_entry.get()
        location = location_entry.get()
        qty = int(qty_entry.get())

        # Check if the component is already in the inventory
        component_exists = False
        for i, row in enumerate(inventory):
            if row[1] == name and row[0] == location:
                inventory[i][2] = str(int(inventory[i][2]) + qty)
                component_exists = True

        # If the component is not in the inventory, add it
        if not component_exists:
            inventory.append([location, name, str(qty)])

        # Update the inventory table and write the inventory to the file
        update_inventory_table()
        write_inventory()

        # Close the Input popup
        input_popup.destroy()

    # Create the Submit button
    submit_button = tk.Button(input_popup, text='Change', command=submit_qty)
    submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create the inventory tab
inventory_frame = tk
# Create the inventory tab
inventory_frame = tk.Frame(root)

# Add the inventory table
update_inventory_table()
inventory_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Add the "Add or Adjust Qty" button
add_or_adjust_button = tk.Button(root, text='Add or Adjust Qty', command=add_or_adjust_qty)
add_or_adjust_button.pack(side='bottom', padx=10, pady=10)

# Create the main loop to run the tkinter application
root.mainloop()
