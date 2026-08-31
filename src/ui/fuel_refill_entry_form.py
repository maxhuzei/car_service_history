import tkinter as tk 
import tkinter.ttk as ttk
from dateutil import parser
from src.ui.add_item_form import AddItemPopup
from src.classes.fuel_reill_entry import FuelRefillEntry
from tkinter import messagebox 

class FuelRefillForm(tk.Frame): 
    def __init__(self, root, controller): 
        super().__init__(root)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        # Injecting the FuelRefillEntry class TODO - add when class will be created
        self.fuel_refill = FuelRefillEntry

        # create and place the main menu frame 
        self.main_menu_frame = tk.Frame(self) 
        self.main_menu_frame.grid(row=0, column=0, sticky='nsew')
        self._create_main_menu(self.main_menu_frame)


        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=1, column=0, sticky='nsew')
        self._create_content_frame(self.content_frame)

    def _create_main_menu(self, root:tk.Frame):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        back_button = ttk.Button(
            root, 
            text="Back", 
            command=lambda: self.controller.switch_form("home") 
        )
        back_button.grid(row=0, column=0, sticky='e', pady=10)


    def _create_content_frame(self, root:tk.Frame): 
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        # create a container for buttons 
        buttons_frame = tk.Frame(root)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        add_new_btn = ttk.Button(
            buttons_frame, 
            text="Add New Fuel Refill",
            command=lambda: self._call_add_update_item_popup(upd=False)
        )
        add_new_btn.grid(row=0, column=0, padx=(0, 10), sticky='w')

        update_item_btn = ttk.Button(
            buttons_frame,
            text="Update Fuel Refill", 
            command=lambda: self._call_add_update_item_popup(upd=True)
        )
        update_item_btn.grid(row=0, column=1, padx=(0,10), sticky='w')

        delete_item_btn = ttk.Button(
            buttons_frame,
            text="Delete Fuel Refill"
        )
        delete_item_btn.grid(row=0, column=2, padx=(0,10), sticky='w')


        # create a container table
        content = tk.Frame(root)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        content.grid(row=1, column=0, sticky='nsew')
        
        # treeview table for fuel refills
        columns = ('id', 'refill_date', 'current_mileage',
                   'fuel_amount', 'fuel_cost', 'avg_consumption')
        self.fuel_refill_tree = ttk.Treeview(
            content, 
            columns=columns, 
            show='headings',
            height=15
        )
        self.fuel_refill_tree.heading('id', text="ID")
        self.fuel_refill_tree.heading('refill_date', text='Refill Date')
        self.fuel_refill_tree.heading('current_mileage', text= "Current Mileage")
        self.fuel_refill_tree.heading('fuel_amount', text="Fuel Amount")
        self.fuel_refill_tree.heading('fuel_cost', text="Fuel Cost")
        self.fuel_refill_tree.heading('avg_consumption', text="Avg Consumption")

        self.fuel_refill_tree.column('id', width=50, anchor='e')
        self.fuel_refill_tree.column('refill_date', width=140, anchor='e')
        self.fuel_refill_tree.column("current_mileage", width=160, anchor='e')
        self.fuel_refill_tree.column('fuel_amount', width=120, anchor='e')
        self.fuel_refill_tree.column('fuel_cost', width=100, anchor='e')
        self.fuel_refill_tree.column('avg_consumption', width=180, anchor='e')
        
        self.fuel_refill_tree.grid(row=0, column=0, sticky='nsew')

        # add vertical scrollbar
        vsb = ttk.Scrollbar(
            content, 
            orient='vertical',
            command=self.fuel_refill_tree.yview
        )
        vsb.grid(row=0, column=1, sticky='w')
        self.fuel_refill_tree.configure(yscrollcommand=vsb.set)

        self._construct_catalog_table(self.fuel_refill_tree, FuelRefillEntry)

    def _call_add_update_item_popup(self, upd:bool=False):
        parent = self
        type = 'fuel_entry'
        fields_list = {
            "refuel_date": ["Refuel Date", 'date'],
            "current_mileage": ["Current Mileage", "str"],
            "refuel_amount": ["Refuel Amount", "str"],
            "refuel_cost": ["Refuel Cost", "str"]
        }

        if not upd:
            title = "Add New Fuel Refill" 
            AddItemPopup(
                parent=parent,
                type=type, 
                title=title,
                fields=fields_list,
                on_submit=self._add_update_item_callback
                )

        if upd:
            # validate if exactly one item is selected, inform user otherwise
            selected_items = self.fuel_refill_tree.selection()
            if len(selected_items) <= 0: 
                messagebox.showinfo(
                    title="Notification",
                    message="Select item to be modified!"
                )
                
            elif len(selected_items) > 1: 
              messagebox.showinfo(
                  title="Notification", 
                  message="Cannot update more then 1 item at once!"
              )  
            else:             
                title = "Update fuel refill entry"
                item_id = int(self.fuel_refill_tree.item(selected_items[0], 'values')[0])
                obj = self.fuel_refill.get_by_id(item_id)
                AddItemPopup(
                    parent=parent,
                    type=type, 
                    title=title,
                    fields=fields_list,
                    on_submit=self._add_update_item_callback,
                    obj=obj
                    )

    def _add_update_item_callback(self, type, entry_data, obj:FuelRefillEntry|None=None):
        if obj is None: 
            refill = FuelRefillEntry(
                parser.parse(entry_data['refuel_date']),
                entry_data["current_mileage"],
                entry_data["refuel_amount"], 
                entry_data["refuel_cost"]
            )
            refill.save()
        else: 
            refill = obj
            refill.refuel_date = parser.parse(entry_data["refuel_date"])
            refill.current_mileage = entry_data["current_mileage"]
            refill.refuel_amount = entry_data["refuel_amount"]
            refill.refuel_cost = entry_data["refuel_cost"]
        refill.save()
        self._construct_catalog_table(self.fuel_refill_tree, FuelRefillEntry)


    def _construct_catalog_table(self, tree_obj:ttk.Treeview, class_obj: type[FuelRefillEntry]) -> None:
        for item in tree_obj.get_children():
            tree_obj.delete(item)

        for item in class_obj.get_all()[::-1]: 
            tree_obj.insert(
                "", 'end', values=(item.id, 
                                   item.refuel_date.date(), 
                                   item.current_mileage,
                                   item.refuel_amount,
                                   item.refuel_cost,
                                   item.calculate_consumption())
            )