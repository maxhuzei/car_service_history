import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from src.classes.general_settings import GeneralSettings
from src.classes.error_code import ErrorCode
from src.classes.maintenance_type import MaintenanceType
from src.classes.db_record import Record
from src.ui.add_item_form import AddItemPopup



class SettingsForm(ttk.Frame):
    def __init__(self, root, controller) -> None:
        super().__init__(root)
        self.controller = controller

        # inject the classes required for settings creation
        self.general_settings = GeneralSettings()
        self.error_code = ErrorCode
        self.maintenance_types = MaintenanceType

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)        
        
        # Back button to return to the home form
        self.back_btn = ttk.Button(
            self, text="Back", command=lambda: self.controller.switch_form("home")
        )
        self.back_btn.grid(row=0, column=0, sticky='e', pady=10)

        # Create the main notebook (tab container)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky='nsew', pady=10)

        # Build the three tabs
        self._build_general_settings_tab()
        self._build_error_codes_tab()
        self._build_maintenance_types_tab()



    # ------------------------------------------------------------------ #
    #  TAB 1 – General Settings
    # ------------------------------------------------------------------ #
    def _build_general_settings_tab(self) -> None:
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General Settings")

        # Car model
        ttk.Label(self.general_tab, text="Car Model:").grid(
            row=0, column=0, padx=10, pady=(20, 5), sticky=tk.W
        )
        self.car_model_var = tk.StringVar()
        self.car_model_var.set(self.general_settings.car_model)
    
        self.car_model_entry = ttk.Entry(
            self.general_tab, textvariable=self.car_model_var, width=50
        )
        self.car_model_entry.grid(row=0, column=1, padx=10, pady=(20, 5), sticky=tk.W)
        # self.car_model_entry.insert(0, self.general_settings.car_model)

        # Max fuel amount
        ttk.Label(self.general_tab, text="Max Fuel Amount:").grid(
            row=1, column=0, padx=10, pady=5, sticky=tk.W
        )
        self.max_fuel_var = tk.StringVar()
        self.max_fuel_var.set(self.general_settings.max_fuel_ammount)

        self.max_fuel_entry = ttk.Entry(
            self.general_tab,  textvariable=self.max_fuel_var, width=50
        )
        self.max_fuel_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Button(self.general_tab, text="Save", command=self._save_general_settings).grid(
            row=2, column=1, sticky='se', padx=10, pady=10
        )

    # ------------------------------------------------------------------ #
    #  TAB 2 – Error Codes
    # ------------------------------------------------------------------ #
    def _build_error_codes_tab(self) -> None:
        self.error_codes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.error_codes_tab, text="Error Codes")

        # -- Button row --
        btn_frame = ttk.Frame(self.error_codes_tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=(10, 5))


        self.add_error_code_btn = ttk.Button(
            btn_frame, 
            text="Add New Error Code", 
            command=lambda: self._call_add_update_item_popup(upd=False)
            )
        
        self.add_error_code_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.update_error_code_btn = ttk.Button(
            btn_frame, 
            text="Update Error Code",
            command=lambda: self._call_add_update_item_popup(upd=True)
        )
        self.update_error_code_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.delete_error_code_btn = ttk.Button(
            btn_frame, text="Delete Error Code", command=self._delete_item_from_table
        )
        self.delete_error_code_btn.pack(side=tk.LEFT, padx=(0, 10))

        # -- Treeview table for error codes --
        columns = ("id", "error_code", "description")
        self.error_codes_tree = ttk.Treeview(
            self.error_codes_tab, columns=columns, show="headings", height=15
        )

        self.error_codes_tree.heading("id", text="ID")
        self.error_codes_tree.heading("error_code", text="Error Code")
        self.error_codes_tree.heading("description", text="Description")

        self.error_codes_tree.column("id", width=60, anchor=tk.CENTER)
        self.error_codes_tree.column("error_code", width=200, anchor=tk.W)
        self.error_codes_tree.column("description", width=400, anchor=tk.W)

        self.error_codes_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Optional: vertical scrollbar
        vsb = ttk.Scrollbar(
            self.error_codes_tab, orient=tk.VERTICAL, command=self.error_codes_tree.yview
        )
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.error_codes_tree.configure(yscrollcommand=vsb.set)
        
        # fill the error code table with items
        self._construct_catalog_table(self.error_codes_tree, ErrorCode)

    # ------------------------------------------------------------------ #
    #  TAB 3 – Maintenance Types
    # ------------------------------------------------------------------ #
    def _build_maintenance_types_tab(self) -> None:
        self.maintenance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.maintenance_tab, text="Maintenance Types")

        # -- Button row --
        btn_frame = ttk.Frame(self.maintenance_tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.add_maintenance_type_btn = ttk.Button(
            btn_frame, 
            text="Add New Maintenance Type",
            command=lambda: self._call_add_update_item_popup(upd=False)
        )
        self.add_maintenance_type_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_maintenance_type_btn = ttk.Button(
            btn_frame, 
            text="Update Error Code",
            command=lambda: self._call_add_update_item_popup(upd=True)
        )
        self.update_maintenance_type_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.delete_maintenance_type_btn = ttk.Button(
            btn_frame, text="Delete Error Code", command=self._delete_item_from_table
        )
        self.delete_maintenance_type_btn.pack(side=tk.LEFT, padx=(0, 10))

        # -- Treeview table for maintenance types --
        columns = ("id", "maintenance_type", "description")
        self.maintenance_types_tree = ttk.Treeview(
            self.maintenance_tab, columns=columns, show="headings", height=15
        )

        self.maintenance_types_tree.heading("id", text="ID")
        self.maintenance_types_tree.heading("maintenance_type", text="Maintenance Type")
        self.maintenance_types_tree.heading("description", text="Description")

        self.maintenance_types_tree.column("id", width=60, anchor=tk.CENTER)
        self.maintenance_types_tree.column("maintenance_type", width=200, anchor=tk.W)
        self.maintenance_types_tree.column("description", width=400, anchor=tk.W)

        self.maintenance_types_tree.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(5, 10)
        )

        # Optional: vertical scrollbar
        vsb = ttk.Scrollbar(
            self.maintenance_tab,
            orient=tk.VERTICAL,
            command=self.maintenance_types_tree.yview,
        )
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.maintenance_types_tree.configure(yscrollcommand=vsb.set)

        # fill the table with items 
        self._construct_catalog_table(self.maintenance_types_tree, MaintenanceType)
    # ------------------------------------------------------------------ #
    #  HELPER FUNCTIONS
    # ------------------------------------------------------------------ #
    def _save_general_settings(self) -> None: 
            # validate if car model is not empty
            if self.car_model_var.get() is not None and self.car_model_var.get().strip() != "":
                _new_car_model = self.car_model_var.get()        
            else:
                raise ValueError("Car model field cannot be empty")

            # validate and assign the max fuel tank ammount
            # validate if convertable to int
            try:
                _max_fuel_var = int(self.max_fuel_var.get().strip())
            except (ValueError, TypeError) as e: 
                raise e 

            # validate if not empty and greater than zero
            if _max_fuel_var is not None and _max_fuel_var > 0:
                _new_max_fuel_ammount = _max_fuel_var
            else: 
                raise ValueError("Max fuel ammount should be more than 0 and not empty!")
            
            self.general_settings.car_model = _new_car_model
            self.general_settings.max_fuel_ammount = _new_max_fuel_ammount

            self.general_settings.save()

    def _construct_catalog_table(self, tree_obj:ttk.Treeview, class_obj: type[ErrorCode]|type[MaintenanceType]) -> None:
        for item in tree_obj.get_children():
            tree_obj.delete(item)

        if class_obj is ErrorCode:
            for item in class_obj.get_all(): 
                tree_obj.insert(
                    "", 'end', values=(item.id, item.error_code, item.description)
                )
        if class_obj is MaintenanceType: 
            for item in class_obj.get_all():
                tree_obj.insert(
                    "", "end", values=(item.id, item.maintenance_type, item.description)
                )

    def _call_add_update_item_popup(self, upd:bool) -> None: 
        # field and type is not required, determine from the tab from which it was called 
        # on_sumbit should be refactored and process both types 
        def _update_item(tree_obj:ttk.Treeview, 
                         class_obj:type[ErrorCode]|type[MaintenanceType], 
                         parent:ttk.Frame,
                         title:str, 
                         fields:tuple|list,
                         on_submit) -> None:
            table_ids = tree_obj.selection()
            
            # chech if items are selected 
            if len(table_ids) == 0: 
                messagebox.showinfo(
                    title="Notification", 
                    message="Select item to update"
                )
                return 
            
            # check if more that one item is selected 
            if len(table_ids) > 1: 
                messagebox.showinfo(
                    title="Notification", 
                    message="Cannot update more than 1 item at once"
                )
                return 
            
            # get selected item id
            item_id = int(tree_obj.item(table_ids[0], 'values')[0])
            obj = class_obj.get_by_id(item_id)
            if isinstance(obj, ErrorCode): 
                type = 'error_code'
            elif isinstance(obj, MaintenanceType):
                type = "maintenance_type"
            else: 
                raise ValueError("Object is not found in the database")
            
            AddItemPopup(
                parent=parent, 
                type=type,
                title=title,
                fields=fields,
                on_submit=on_submit,
                obj=obj
            )
            
            self._construct_catalog_table(tree_obj, class_obj)

        tab_text = self.notebook.tab(self.notebook.select()).get("text")
        if tab_text == "Error Codes":
            fields = ('error_code', 'description')
            parent = self.error_codes_tab
            if upd is False: 
                title = "Add New Error Code"
                AddItemPopup(parent=parent, 
                            type="error_code",
                            title=title, 
                            fields=fields,
                            on_submit=self._add_new_item_callback)
                # update table to show the recent items
                
            if upd is True: 
                title = "Update Error Code"
                _update_item(
                    tree_obj=self.error_codes_tree, 
                    class_obj=ErrorCode, 
                    parent=parent,
                    title=title,
                    fields=fields,
                    on_submit=self._update_item_callback
                )
                
        if tab_text == "Maintenance Types": 
            fields = ("maintenance_type", "description")
            parent = self.maintenance_tab
            if upd is False: 
                title = "Add New Maintenance Type"
                AddItemPopup(
                    parent=parent,
                    type="maintenance_type",
                    title=title,
                    fields=fields,
                    on_submit=self._add_new_item_callback
                )

                # update table to show the latest items
                self._construct_catalog_table(self.maintenance_types_tree, MaintenanceType)

            if upd is True: 
                title = "Update Maintenance Type"
                _update_item(
                    tree_obj=self.maintenance_types_tree, 
                    class_obj=MaintenanceType, 
                    parent=parent,
                    title=title,
                    fields=fields,
                    on_submit=self._update_item_callback
                )

            

    def _add_new_item_callback(self, type:str, entries:dict, obj=None) -> None:
        tree_obj, class_obj = None, None
        if type == "error_code": 
            obj = ErrorCode(entries['error_code'], entries["description"])
            tree_obj = self.error_codes_tree
            class_obj = ErrorCode

        elif type == "maintenance_type":
            obj = MaintenanceType(entries["maintenance_type"], entries["description"])
            tree_obj = self.maintenance_types_tree
            class_obj = MaintenanceType

        else: 
            raise ValueError("Type must be one of (error_code, maintenance_type)")
        
        obj.save()
        if tree_obj is not None and class_obj is not None: 
            self._construct_catalog_table(tree_obj, class_obj)

        
    def _update_item_callback(self, type:str, entries:dict, obj:ErrorCode|MaintenanceType) -> None:
        tree_obj, class_obj = None, None
        if isinstance(obj, ErrorCode): 
            obj.error_code = entries['error_code']
            obj.description = entries['description']
            tree_obj = self.error_codes_tree
            class_obj = ErrorCode
            
        if isinstance(obj, MaintenanceType):
            obj.maintenance_type = entries["maintenance_type"]
            obj.description = entries["description"]
            tree_obj = self.maintenance_types_tree
            class_obj = MaintenanceType
        
        obj.save()
        if tree_obj is not None and class_obj is not None: 
            self._construct_catalog_table(tree_obj, class_obj)


        # self._construct_catalog_table()

    def _delete_item_from_table(self) -> None: 
        # func to delete item not depending on tab
        def _delete_item(tree_obj:ttk.Treeview, class_obj:type[ErrorCode]|type[MaintenanceType]) -> None: 
            # get and remove the selected items
            table_item_ids = tree_obj.selection()

            if len(table_item_ids) > 0: 
            # check if removal is required 
                confirm = messagebox.askokcancel(
                    title="Confirm deletion",
                    message="Do you want to delete selected items?",
                    icon="warning"
                )
                if not confirm:
                    return
            else: 
                messagebox.showinfo(
                    title="Notification",
                    message="Select an items to be deleted"
                )


            for item in table_item_ids: 
                item_id = int(tree_obj.item(item, 'values')[0])
                obj = class_obj.get_by_id(item_id)
                if isinstance(obj, (ErrorCode, MaintenanceType)): 
                    obj.delete()
            
            # reconstruct the table after deletion
            self._construct_catalog_table(tree_obj, class_obj)
            
        # call the delete function based on tab from which it's called
        tab_text = self.notebook.tab(self.notebook.select()).get("text")

        if tab_text == "Error Codes": 
            _delete_item(self.error_codes_tree, ErrorCode)

        if tab_text == "Maintenance Types":
            _delete_item(self.maintenance_types_tree, MaintenanceType)