import tkinter as tk
import csv

# Define the column names for the inventory table
inventory_columns = ['Location', 'Name', 'Qty']

# Define the filename where the inventory will be saved
inventory_filename = 'inventory.csv'

# Create the main tkinter window
root = tk.Tk()
root.title('Arduino Inventory')

# Define a function to read the inventory from the CSV file
def read_inventory():
    try:
        with open(inventory_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            inventory = [row for row in reader]
    except FileNotFoundError:
        inventory = []
    return inventory

# Define a function to write the inventory to the CSV file
def write_inventory(inventory):
    with open(inventory_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(inventory)

# Define a function to update the inventory table
def update_inventory_table():
    # Clear the existing table
    for widget in inventory_frame.winfo_children():
        widget.destroy()

    # Add the column headers
    for i, column_name in enumerate(inventory_columns):
        column_label = tk.Label(inventory_frame, text=column_name)
        column_label.grid(row=0, column=i, padx=5, pady=5)

    # Add the inventory rows
    inventory = read_inventory()
    for i, item in enumerate(inventory):
        for j, value in enumerate(item):
            item_label = tk.Label(inventory_frame, text=value)
            item_label.grid(row=i+1, column=j, padx=5, pady=5)

# Define a function to handle adding or adjusting quantities
def add_or_adjust_qty():
    # Define a function to handle the "Change" button click
    def change_qty():
        # Get the component name and change in quantity from the input fields
        component_name = component_name_entry.get()
        qty_change = int(qty_change_entry.get())

        # Update the inventory with the new quantity
        inventory = read_inventory()
        for item in inventory:
            if item[1] == component_name:
                item[2] = str(int(item[2]) + qty_change)
                break
        else:
            inventory.append(['', component_name, str(qty_change)])
        write_inventory(inventory)

        # Update the inventory table
        update_inventory_table()

        # Close the input window
        input_window.destroy()

    # Create the input window
    input_window = tk.Toplevel(root)
    input_window.title('Add or Adjust Qty')

    # Add the component name input field
    component_name_label = tk.Label(input_window, text='Component Name:')
    component_name_label.grid(row=0, column=0, padx=5, pady=5)
    component_name_entry = tk.Entry(input_window)
    component_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Add the quantity change input field
    qty_change_label = tk.Label(input_window, text='Qty Change:')
    qty_change_label.grid(row=1, column=0, padx=5, pady=5)
    qty_change_entry = tk.Entry(input_window)
    qty_change_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add the "Change" button
    change_button = tk.Button(input_window, text='Change', command=change_qty)
    change_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

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
