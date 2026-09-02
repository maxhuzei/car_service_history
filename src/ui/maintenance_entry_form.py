import tkinter as tk 
import tkinter.ttk as ttk
from src.ui.add_item_form import AddItemPopup
from src.classes.maintenance_entry import MaintenanceEntry
from src.classes.maintenance_type import MaintenanceType
from tkinter import messagebox 

class MaintenanceEntryForm(tk.Frame): 
    def __init__(self, root, controller): 
        super().__init__(root)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        # Injecting the MaintenanceEntry class
        self.maintenance_entry = MaintenanceEntry

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
            text="Add New Maintenance Entry",
            command=lambda: self._call_add_update_item_popup(upd=False)
        )
        add_new_btn.grid(row=0, column=0, padx=(0, 10), sticky='w')

        update_item_btn = ttk.Button(
            buttons_frame,
            text="Update Maintenance Entry", 
            command=lambda: self._call_add_update_item_popup(upd=True)
        )
        update_item_btn.grid(row=0, column=1, padx=(0,10), sticky='w')

        delete_item_btn = ttk.Button(
            buttons_frame,
            text="Delete Maintenance Entry",
            command=self._delete_items
        )
        delete_item_btn.grid(row=0, column=2, padx=(0,10), sticky='w')


        # create a container table
        content = tk.Frame(root)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        content.grid(row=1, column=0, sticky='nsew')
        
        # treeview table for maintenance entries
        columns = ('id', 'date_created', 'maintenance_event',
                   'dtc_code', 'symptoms', 'comment', 'cost')
        self.maintenance_entry_tree = ttk.Treeview(
            content, 
            columns=columns, 
            show='headings',
            height=15
        )
        self.maintenance_entry_tree.heading('id', text="ID")
        self.maintenance_entry_tree.heading('date_created', text='Date Created')
        self.maintenance_entry_tree.heading('maintenance_event', text= "Maintenance Type")
        self.maintenance_entry_tree.heading('dtc_code', text="DTC Code")
        self.maintenance_entry_tree.heading('symptoms', text="Symptoms")
        self.maintenance_entry_tree.heading('comment', text="Comment")
        self.maintenance_entry_tree.heading('cost', text="Cost")

        self.maintenance_entry_tree.column('id', width=50, anchor='e')
        self.maintenance_entry_tree.column('date_created', width=150, anchor='e')
        self.maintenance_entry_tree.column('maintenance_event', width=160, anchor='w')
        self.maintenance_entry_tree.column('dtc_code', width=100, anchor='w')
        self.maintenance_entry_tree.column('symptoms', width=220, anchor='w')
        self.maintenance_entry_tree.column('comment', width=220, anchor='w')
        self.maintenance_entry_tree.column('cost', width=100, anchor='e')
        
        self.maintenance_entry_tree.grid(row=0, column=0, sticky='nsew')

        # add vertical scrollbar
        vsb = ttk.Scrollbar(
            content, 
            orient='vertical',
            command=self.maintenance_entry_tree.yview
        )
        vsb.grid(row=0, column=1, sticky='w')
        self.maintenance_entry_tree.configure(yscrollcommand=vsb.set)

        self._construct_catalog_table(self.maintenance_entry_tree, MaintenanceEntry)

    def _call_add_update_item_popup(self, upd:bool=False):
        parent = self
        type = 'maintenance_entry'
        maintenance_types = [mt.maintenance_type for mt in MaintenanceType.get_all()]
        fields_list = {
            "maintenance_event": ["Maintenance Type", "dropdown", maintenance_types],
            "dtc_code": ["DTC Code", "str", 5],
            "symptoms": ["Symptoms", "str", 500],
            "comment": ["Comment", "str", 500],
            "cost": ["Cost", "float"]
        }

        if not upd:
            title = "Add New Maintenance Entry" 
            AddItemPopup(
                parent=parent,
                type=type, 
                title=title,
                fields=fields_list,
                on_submit=self._add_update_item_callback
                )

        if upd:
            # validate if exactly one item is selected, inform user otherwise
            selected_items = self.maintenance_entry_tree.selection()
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
                title = "Update Maintenance Entry"
                item_id = int(self.maintenance_entry_tree.item(selected_items[0], 'values')[0])
                obj = self.maintenance_entry.get_by_id(item_id)
                AddItemPopup(
                    parent=parent,
                    type=type, 
                    title=title,
                    fields=fields_list,
                    on_submit=self._add_update_item_callback,
                    obj=obj
                    )

    def _add_update_item_callback(self, type, entry_data, obj:MaintenanceEntry|None=None):
        maintenance_event = entry_data["maintenance_event"]
        dtc_code = entry_data["dtc_code"].strip()
        symptoms = entry_data["symptoms"].strip()
        comment = entry_data["comment"].strip()

        # data entry validation
        if not maintenance_event: 
            raise ValueError("Maintenance type must be selected from the catalog!")
        if len(dtc_code) > 5: 
            raise ValueError("DTC code cannot be longer than 5 symbols!")
        if len(symptoms) > 500: 
            raise ValueError("Symptoms cannot be longer than 500 symbols!")
        if len(comment) > 500: 
            raise ValueError("Comment cannot be longer than 500 symbols!")
        try: 
            cost = float(entry_data["cost"])
        except ValueError: 
            raise ValueError("Cost must be a floating point number!")

        if obj is None: 
            maintenance = MaintenanceEntry(
                maintenance_event=maintenance_event,
                dtc_code=dtc_code,
                symptoms=symptoms,
                comment=comment,
                cost=cost
            )
            maintenance.save()
        else: 
            maintenance = obj
            maintenance.maintenance_event = maintenance_event
            maintenance.dtc_code = dtc_code
            maintenance.symptoms = symptoms
            maintenance.comment = comment
            maintenance.cost = cost
            maintenance.save()
        self._construct_catalog_table(self.maintenance_entry_tree, MaintenanceEntry)

    def _delete_items(self):
        table_item_ids = self.maintenance_entry_tree.selection()
        if len(table_item_ids) > 0: 
            confirm = messagebox.askokcancel(
                title="Confirm deletion",
                message="Are you sure you want to delete the selected items?",
                icon="warning"
            )

            if not confirm:
                return 
        else:
            messagebox.showinfo(
                title="No item selected!",
                message="Select an item to be deleted!"
            )
            return

        for item in table_item_ids: 
            item_id = int(self.maintenance_entry_tree.item(item, 'values')[0])
            obj = self.maintenance_entry.get_by_id(item_id)
            obj.delete()

        self._construct_catalog_table(self.maintenance_entry_tree, self.maintenance_entry)


    def _construct_catalog_table(self, tree_obj:ttk.Treeview, class_obj: type[MaintenanceEntry]) -> None:
        for item in tree_obj.get_children():
            tree_obj.delete(item)

        for item in class_obj.get_all(): 
            tree_obj.insert(
                "", 'end', values=(item.id, 
                                   item.date_created.date() if item.date_created is not None else "",
                                   item.maintenance_event,
                                   item.dtc_code,
                                   item.symptoms,
                                   item.comment,
                                   item.cost)
            )
