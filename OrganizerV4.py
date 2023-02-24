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
    def __init__(self, master):
        self.master = master
        self.master.title('Inventory App')
        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        # Define tree as a class-level variable
        self.tree = ttk.Treeview(self.frame)

        # Define columns for the tree
        self.tree['columns'] = ('Description', 'Quantity', 'Price', 'Category')

        # Format the columns
        self.tree.column('#0', width=0, stretch='no')
        self.tree.column('Description', anchor='center', width=200)
        self.tree.column('Quantity', anchor='center', width=100)
        self.tree.column('Price', anchor='center', width=100)
        self.tree.column('Category', anchor='center', width=100)

        # Create column headings
        self.tree.heading('#0', text='', anchor='w')
        self.tree.heading('Description', text='Description', anchor='center')
        self.tree.heading('Quantity', text='Quantity', anchor='center')
        self.tree.heading('Price', text='Price', anchor='center')
        self.tree.heading('Category', text='Category', anchor='center')

        # Add the tree to the frame
        self.tree.pack()

        # Create a scrollbar for the tree
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Add buttons to the frame
        self.add_button = ttk.Button(self.frame, text='Add Item', command=self.show_add_item_popup)
        self.add_button.pack(side='left')
        self.edit_button = ttk.Button(self.frame, text='Edit Item', command=self.show_edit_item_popup)
        self.edit_button.pack(side='left')
        self.delete_button = ttk.Button(self.frame, text='Delete Item', command=self.delete_item)
        self.delete_button.pack(side='left')

        # Load the inventory data into the table
        self.populate_table()

    def populate_table(self):
        # Clear any existing items in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load the inventory data from the file
        inventory_data = self.load_inventory_data()

        # Add the inventory data to the table
        for i, item in enumerate(inventory_data):
            row = (item['description'], item['quantity'], item['price'], item['category'])
            self.tree.insert(parent='', index='end', iid=i, values=row)

    def update_table(self):
        # Clear the existing items in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Re-populate the table with the updated inventory data
        self.populate_table()

    def show_add_item_popup(self):
        # Code for showing the add item popup goes here
        pass

    def show_edit_item_popup(self):
        # Code for showing the edit item popup goes here
        pass
    def show_edit_item_popup(self):
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showwarning("Error", "Please select an item to edit.")
                return
            item_values = self.tree.item(selected_item, "values")
            item_name = item_values[0]
            item_quantity = item_values[1]
            item_price = item_values[2]
            item_category = item_values[3]
            # Create a new popup window
            edit_item_popup = Toplevel()
            edit_item_popup.title("Edit Item")
            edit_item_popup.geometry("400x300")
            # Add labels and entry fields to the popup window
            name_label = Label(edit_item_popup, text="Name:")
            name_label.grid(row=0, column=0, padx=10, pady=10)
            name_entry = Entry(edit_item_popup)
            name_entry.grid(row=0, column=1, padx=10, pady=10)
            name_entry.insert(END, item_name)
            quantity_label = Label(edit_item_popup, text="Quantity:")
            quantity_label.grid(row=1, column=0, padx=10, pady=10)
            quantity_entry = Entry(edit_item_popup)
            quantity_entry.grid(row=1, column=1, padx=10, pady=10)
            quantity_entry.insert(END, item_quantity)
            price_label = Label(edit_item_popup, text="Price:")
            price_label.grid(row=2, column=0, padx=10, pady=10)
            price_entry = Entry(edit_item_popup)
            price_entry.grid(row=2, column=1, padx=10, pady=10)
            price_entry.insert(END, item_price)
            category_label = Label(edit_item_popup, text="Category:")
            category_label.grid(row=3, column=0, padx=10, pady=10)
            category_entry = ttk.Combobox(edit_item_popup, values=self.categories)
            category_entry.grid(row=3, column=1, padx=10, pady=10)
            category_entry.insert(END, item_category)
            # Add a Save button to the popup window
            save_button = Button(edit_item_popup, text="Save",
                                 command=lambda: self.save_edited_item(selected_item, name_entry.get(), quantity_entry.get(), price_entry.get(), category_entry.get(), edit_item_popup))
            save_button.grid(row=4, column=1, padx=10, pady=10)

def main():
    # create the inventory window
    inventory_window = create_inventory_window()

    # create the input window
    input_window = create_input_window(inventory_window)

    # create the revision log window
    # This function creates a new window to display a table of all revisions to the inventory levels.
    # It reads the revision log from file and creates a table using tkinter's Treeview widget.
    # The table has four columns: Component Name, New Quantity, Quantity Change, and Timestamp.
    # The table is sorted in descending order by timestamp so that the most recent changes are displayed first.
    # The function also creates a scrollbar to allow scrolling through the table if there are many revisions.
    # The window is displayed using tkinter's mainloop() function.
    revision_window = create_revision_window()

    # read the inventory from file
    inventory = read_inventory_from_file()

    # update the table with the current inventory
    update_inventory_table(inventory_window, inventory)

    # run the main loop
    inventory_window.mainloop()

if __name__ == '__main__':
    main()
