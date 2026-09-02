import tkinter as tk
from tkinter import ttk


class HomeForm(ttk.Frame):
    def __init__(self, root, controller) -> None:
        super().__init__(root)
        self.controller = controller

        # centering the child Frame to get content in the middle
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # building the content of the child frame 
        self._build_home_form()


    def _build_home_form(self) -> None: 

        # Center frame holding the content, placed in the middle of the form
        center_frame = ttk.Frame(self)
        center_frame.grid(row=1, column=1)

        self.label = ttk.Label(
            center_frame, text="Car Service History", anchor='center'
        )
        self.label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.fuel_button = ttk.Button(
            center_frame, 
            text="Fuel Refill Entry",
            command=lambda: self.controller.switch_form("fuel_refill")
        )
        self.fuel_button.grid(row=1, column=0, padx=10)

        self.maintenance_button = ttk.Button(
            center_frame, text="Maintenance Entry",
            command=lambda: self.controller.switch_form("maintenance_entry")
        )
        self.maintenance_button.grid(row=1, column=1, padx=10)

        self.settings_button = ttk.Button(
            center_frame, 
            text="Settings", 
            command=lambda: self.controller.switch_form("settings")
        )
        self.settings_button.grid(row=1, column=2, padx=10)
