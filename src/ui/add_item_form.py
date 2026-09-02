import tkinter as tk 
import tkinter.ttk as ttk 
from tkinter import messagebox
from src.classes.error_code import ErrorCode
from src.classes.maintenance_type import MaintenanceType
from src.classes.fuel_reill_entry import FuelRefillEntry
from src.classes.maintenance_entry import MaintenanceEntry

class AddItemPopup(tk.Toplevel):
    def __init__(self, parent, type:str, title:str, fields:list|tuple|dict, on_submit, obj:ErrorCode|MaintenanceType|FuelRefillEntry|MaintenanceEntry|None = None) -> None:
        super().__init__(parent) 
        self.title(title)
        self.geometry("960x480")
        self.type = type
        
        # Lock focus to this window
        self.transient(parent)
        self.grab_set()

        # centering the content in the pop-up window 
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        
        # making the only column to stretch for entire form
        self.columnconfigure(0, weight=1)
        
        # put fields and buttons into the surrounding field_container
        self.field_container = ttk.Frame(self)
        self.field_container.grid(row=1, column=0)
        
        # configure grid layout to center the data entry horizontally   
        self.field_container.columnconfigure(0, weight=1)
        self.field_container.columnconfigure(4, weight=1)

        self.entry_data = {} 
        self.entries = {}

        # Convert fields list to dict to avoid changing the old implementations 
        fields_dict = self._convert_field_list(fields)

        for i in range(len(fields_dict)): 
            _key = list(fields_dict.keys())[i]
            _field_spec = fields_dict[_key]
            _label = _field_spec[0]
            _field_type = _field_spec[1] if len(_field_spec) > 1 else 'str'
            _extra = _field_spec[2] if len(_field_spec) > 2 else None

            ttk.Label(
                self.field_container, anchor="w", text=_label, width=20
            ).grid(row=i+1, column=2, padx=(10, 0))

            if _field_type == 'dropdown':
                # dropdown selection, e.g. items from a catalog
                entry = ttk.Combobox(
                    self.field_container,
                    values=_extra if isinstance(_extra, (list, tuple)) else (),
                    state='readonly',
                    width=28
                )
                if obj is not None: 
                    entry.set(str(obj.__dict__.get(_key)))
            else: 
                entry = ttk.Entry(
                    self.field_container, width=30
                )
                if isinstance(_extra, int) and _extra > 0: 
                    # limit the amount of symbols that can be typed in
                    entry.configure(
                        validate='key',
                        validatecommand=(self.register(self._validate_max_length), '%P', _extra)
                    )
                if obj is not None: 
                    entry.insert(0, str(obj.__dict__.get(_key)))

            entry.grid(row=i+1, column=3, padx=10)
            self.entries[_key] = entry
        # create an additional containers to hold the buttons 
        self.buttons_container = ttk.Frame(self)
        self.buttons_container.grid(row=2, column=0)

        # configure grid layout to center the content vertically and horizontally 
        self.buttons_container.rowconfigure(0, weight=1)
        self.buttons_container.rowconfigure(3, weight=1)
        self.buttons_container.columnconfigure(0, weight=1)
        self.buttons_container.columnconfigure(4, weight=1)

        # create the buttons 
        ttk.Button( 
            self.buttons_container, 
            text="Cancel", 
            command=self._on_cancel   
        ).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(20, 10))

        ttk.Button(
            self.buttons_container, 
            text="Submit", 
            command=lambda: self._on_submit(on_submit=on_submit, obj=obj)
        ).grid(row=1, column=2, sticky="w", padx=(0, 20), pady=(20, 10))


    def _on_cancel(self):
        # close the widget
        self.destroy()

    def _on_submit(self,  on_submit, obj=None): 
        # read the data from the Entry entities dynamically 
        for item in self.entries.keys():
            self.entry_data[item] = self.entries[item].get()

        # passing it to the callback function 
        try: 
            on_submit(self.type, self.entry_data, obj) 
        except ValueError as e: 
            # keep the pop-up open and inform the user about the validation issue
            messagebox.showinfo(
                title="Validation Error",
                message=str(e)
            )
            return

        # close the widget
        self.destroy()

    def _validate_max_length(self, new_value:str, max_length:str) -> bool: 
        return len(new_value) <= int(max_length)

    def _convert_field_list(self, fields:tuple|list|dict):
        if isinstance(fields, (list, tuple)):
            fields_dict = {}
            for item in fields:
                fields_dict[item] = [item, 'str']
        else: 
            fields_dict = fields 
        return fields_dict