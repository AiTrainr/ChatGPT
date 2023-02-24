import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
from datetime import datetime

INVENTORY_FILE = 'inventory.csv'
REVISION_LOG_FILE = 'revision_log.txt'

class InventoryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Inventory Management System")

class InventoryApp:
    """Main application window for the inventory app."""

    def __init__(self, master):
        self.master = master
        self.master.title('Inventory Application')
        self.create_menu()
        self.inventory_frame = InventoryFrame(self.master) # create an instance of the InventoryFrame widget

    def create_menu(self):
        """Create menu bar for application."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Create file menu
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Add Item', command=self.inventory_frame.show_add_item_popup)
        file_menu.add_command(label='Edit Item', command=self.show_edit_item_popup)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.quit)

        # Create help menu
        help_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.show_about_popup)

    def create_widgets(self):
        """Create and set up widgets for main application window."""
        # Create and set up treeview widget
        self.tree = ttk.Treeview(self.master)
        self.tree.pack(fill='both', expand=True)

        self.tree['columns'] = ('name', 'quantity', 'description')
        self.tree.column('#0', width=0, stretch='no')
        self.tree.column('name', anchor='w', width=150)
        self.tree.column('quantity', anchor='w', width=150)
        self.tree.column('description', anchor='w', width=300)

        self.tree.heading('#0', text='', anchor='w')
        self.tree.heading('name', text='Name', anchor='w')
        self.tree.heading('quantity', text='Quantity', anchor='w')
        self.tree.heading('description', text='Description', anchor='w')

        # Create and set up scrollbar widget
        scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def load_inventory(self):
        """Load inventory data from CSV file and display in treeview."""
        if not os.path.isfile(INVENTORY_FILE):
            return

        # Clear any existing data from the treeview
        self.tree.delete(*self.tree.get_children())

        # Load inventory data from CSV file
        with open(INVENTORY_FILE, newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    continue  # skip header row
                self.tree.insert(parent='', index='end', iid=i, values=row)

    def save_inventory(self):
        """Save inventory data to CSV file."""
        with open(INVENTORY_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Quantity', 'Description'])
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                writer.writerow(values)

    def add_item(self, name, quantity, description):
        """Add item to inventory."""
        self.tree.insert(parent='', index='end', iid='', values=[name, quantity, description])
        self.save_inventory()
        self.log_revision(f'Added item: {name}')
    def remove_item(self):
        """Remove item from inventory."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning('Warning', 'Please select an item to remove.')
            return
        name = self.tree.item(selected_item)['values'][0]
        self.tree.delete(selected_item)
        self.save_inventory()
        self.log_revision(f'Removed item: {name}')

    def edit_item(self):
        """Edit item in inventory."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning('Warning', 'Please select an item to edit.')
            return
        item_name = self.tree.item(selected_item)['values'][0]
        item_quantity = self.tree.item(selected_item)['values'][1]
        item_description = self.tree.item(selected_item)['values'][2]

        # Create a new popup window to edit the item
        self.edit_item_popup = Toplevel()
        self.edit_item_popup.title('Edit Item')
        self.edit_item_popup.geometry('400x200')
        self.edit_item_popup.resizable(False, False)

        # Create labels and entry fields in the popup window
        item_name_label = Label(self.edit_item_popup, text='Name: ', font=('Helvetica', 12))
        item_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        item_name_entry = Entry(self.edit_item_popup, font=('Helvetica', 12))
        item_name_entry.insert(END, item_name)
        item_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        item_quantity_label = Label(self.edit_item_popup, text='Quantity: ', font=('Helvetica', 12))
        item_quantity_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        item_quantity_entry = Entry(self.edit_item_popup, font=('Helvetica', 12))
        item_quantity_entry.insert(END, item_quantity)
        item_quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        item_description_label = Label(self.edit_item_popup, text='Description: ', font=('Helvetica', 12))
        item_description_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        item_description_entry = Entry(self.edit_item_popup, font=('Helvetica', 12))
        item_description_entry.insert(END, item_description)
        item_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # Create a Save button in the popup window to save changes to the item
        save_button = Button(self.edit_item_popup, text='Save', font=('Helvetica', 12), command=lambda: self.save_edited_item(item_name, selected_item, item_name_entry.get(), item_quantity_entry.get(), item_description_entry.get()))
        save_button.grid(row=3, column=1, padx=5, pady=5, sticky=E)

        # Create a Cancel button in the popup window to cancel changes to the item
        cancel_button = Button(self.edit_item_popup, text='Cancel', font=('Helvetica', 12), command=self.edit_item_popup.destroy)
        cancel_button.grid(row=3, column=0, padx=5, pady=5, sticky=W)

    def save_edited_item(self, item_name, selected_item, new_name, new_quantity, new_description):
        # update the selected item with new values
        selected_item['name'] = new_name
        selected_item['quantity'] = new_quantity
        selected_item['description'] = new_description

        # update the treeview with new values
        self.tree.item(item_name, values=[new_name, new_quantity, new_description])

        # save the inventory to file
        self.save_inventory()

        # log the revision
        self.log_revision(f"Edited item: {item_name} -> {new_name}, {selected_item['quantity']} -> {new_quantity}, {selected_item['description']} -> {new_description}")

class InventoryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.add_item_button = tk.Button(self, text='Add Item', command=self.show_add_item_popup)
        self.add_item_button.pack(pady=10, padx=10)

    def show_add_item_popup(self):
        add_item_popup = tk.Toplevel(self.master)
        add_item_popup.title('Add Item')
        # Add code to create the popup

if __name__ == '__main__':
    root = tk.Tk()  # create a new instance of the root window
    app = InventoryApp(root)  # pass the root as the master argument
    app.mainloop()
