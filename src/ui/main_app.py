import tkinter as tk 
import tkinter.ttk as ttk
from src.ui.home_form import HomeForm
from src.ui.settings_form import SettingsForm
from src.ui.fuel_refill_entry_form import FuelRefillForm

class MainApplication: 
    def __init__(self, root: tk.Tk) -> None:
        self.root = root 
        self.root.title("Car Service History")
        self.root.geometry("1600x1200")

        # Configure root window grid so the container fills the window
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.forms = {
             "home": HomeForm, 
             "settings": SettingsForm,
             "fuel_refill": FuelRefillForm
        }

        self.container = ttk.Frame(root)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.grid(row=0, column=0, sticky='nsew')

        self.current_form = None 
        self.switch_form("home")

    def switch_form(self, form_string) -> None:
        # destroy existing form if one is selected
        if self.current_form is not None: 
                self.current_form.destroy()

        # select a form from the list of forms for string based navigation
        _selected_form = self.forms[form_string]
        
        self.current_form = _selected_form(self.container, self)
        self.current_form.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

