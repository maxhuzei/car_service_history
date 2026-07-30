import tkinter as tk 
import tkinter.ttk as ttk

class FuelRefillForm(tk.Frame): 
    def __init__(self, root, controller): 
        super().__init__(root)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        # Injecting the FuelRefillEntry class TODO - add when class will be created
        # self.fuel_refill = 

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
            text="Add New Fuel Refill"
        )
        add_new_btn.grid(row=0, column=0, padx=(0, 10), sticky='w')

        update_item_btn = ttk.Button(
            buttons_frame,
            text="Update Fuel Refill"
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