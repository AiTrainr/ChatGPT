import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from datetime import datetime
import csv
import os


# File paths for inventory and revision log CSV files
INVENTORY_FILE = 'inventory.csv'
REVISION_LOG_FILE = 'revision_log.csv'

# If the inventory file doesn't exist, create it with header row
if not os.path.exists(INVENTORY_FILE):
    with open(INVENTORY_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Location', 'Name', 'Qty'])

# If the revision log file doesn't exist, create it with header row
if not os.path.exists(REVISION_LOG_FILE):
    with open(REVISION_LOG_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'New Qty', 'Qty Change', 'Date/Time'])


class InventoryApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Arduino Component Inventory Tracker')

        # Create tabs for Inventory and Revision Log
        self.tabControl = ttk.Notebook(self.root)
        self.inventoryTab = ttk.Frame(self.tabControl)
        self.revisionLogTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.inventoryTab, text='Inventory')
        self.tabControl.add(self.revisionLogTab, text='Revision Log')
        self.tabControl.pack(expand=1, fill='both')

        # Create Inventory table
        self.inventoryTable = ttk.Treeview(self.inventoryTab, columns=('Location', 'Name', 'Qty'))
        self.inventoryTable.heading('Location', text='Location')
        self.inventoryTable.heading('Name', text='Name')
        self.inventoryTable.heading('Qty', text='Qty')
        self.inventoryTable.column('Location', width=100)
        self.inventoryTable.column('Name', width=250)
        self.inventoryTable.column('Qty', width=50)
        self.inventoryTable.pack(pady=10)

        # Populate Inventory table with data from CSV file
        with open(INVENTORY_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.inventoryTable.insert('', 'end', values=(row['Location'], row['Name'], row['Qty']))

        # Create Add/Adjust Qty button
        self.addAdjustButton = tk.Button(self.inventoryTab, text='Add or Adjust Qty', command=self.openInputPopup)
        self.addAdjustButton.pack(pady=10)

        # Create Revision Log table
        self.revisionLogTable = ttk.Treeview(self.revisionLogTab, columns=('Name', 'New Qty', 'Qty Change', 'Date/Time'))
        self.revisionLogTable.heading('Name', text='Name')
        self.revisionLogTable.heading('New Qty', text='New Qty')
        self.revisionLogTable.heading('Qty Change', text='Qty Change')
        self.revisionLogTable.heading('Date/Time', text='Date/Time')
        self.revisionLogTable.column('Name', width=150)
        self.revisionLogTable.column('New Qty', width=80)
        self.revisionLogTable.column('Qty Change', width=80)
        self.revisionLogTable.column('Date/Time', width=150)
        self.revisionLogTable.pack(pady=10)

        # Populate Revision Log table with data from CSV file
            # Load revision log data
    with open(REVISION_LOG_FILE, 'r') as file:
        data = file.readlines()

        # Remove newline characters from each line and split by comma
        data = [line.strip().split(',') for line in data]

        # Reverse the order of the data list so the most recent revisions are displayed first
        data.reverse()

        # Display the revision log data in the table
        for i, row in enumerate(data):
            tree.insert(parent='', index='end', iid=i, values=row)

    # Configure columns for revision log table
    tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
    tree.column("Name", anchor=tk.W, width=200)
    tree.column("New Quantity", anchor=tk.CENTER, width=100)
    tree.column("Quantity Change", anchor=tk.CENTER, width=150)
    tree.column("Date/Time", anchor=tk.CENTER, width=200)

    # Configure headings for revision log table
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Name", text="Name", anchor=tk.W)
    tree.heading("New Quantity", text="New Quantity", anchor=tk.CENTER)
    tree.heading("Quantity Change", text="Quantity Change", anchor=tk.CENTER)
    tree.heading("Date/Time", text="Date/Time", anchor=tk.CENTER)

    # Add scrollbar to revision log table
    tree_scroll = ttk.Scrollbar(tab2_frame, orient="vertical", command=tree.yview)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Bind the scrollbar to the revision log table
    tree.configure(yscrollcommand=tree_scroll.set)

    # Add labels and entry fields for component name and quantity change to the Input window
    name_label = ttk.Label(input_window, text="Component Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    name_entry = ttk.Entry(input_window, width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    quantity_label = ttk.Label(input_window, text="Quantity Change:")
    quantity_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    quantity_entry = ttk.Entry(input_window, width=25)
    quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # Add a button to the Input window to submit the changes
    change_button = ttk.Button(input_window, text="Change", command=lambda: change_quantity())
    change_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Function to update inventory and revision log with changes
    def change_quantity():
        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the component name and quantity change from the input fields
        component_name = name_entry.get()
        quantity_change = quantity_entry.get()

        # Check if the component exists in the inventory
        for row in tree.get_children():
            if tree.item(row)['values'][0] == component_name:
                # If the component exists, update the quantity
                current_qty = int(tree.item(row)['values'][1])
                new_qty = current_qty + int(quantity_change)
                tree.item(row, values=(component_name, new_qty, quantity_change, current_time))
                break
        else:
            # If the component does not exist, add a
    # write revision to file
    with open(REVISION_LOG_FILE, 'a') as file:
        file.write(f"{name},{new_qty},{change},{current_time}\n")

def main():
    # create the inventory window
    inventory_window = create_inventory_window()

    # create the input window
    input_window = create_input_window(inventory_window)

    # create the revision log window
    revision_window = create_revision_window()

    # read the inventory from file
    inventory = read_inventory_from_file()

    # update the table with the current inventory
    update_inventory_table(inventory_window, inventory)

    # run the main loop
    inventory_window.mainloop()

if __name__ == '__main__':
    main()
