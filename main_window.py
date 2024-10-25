import tkinter as tk
from tkinter import ttk
from navigation_tab import TabbedBrowser

config_boton = {
    "bg": "#4CAF50",
    "fg": "white",
    "font": ("Arial", 10),
    "activebackground": "#45a049",
    "relief": "flat"
}

config_entry = {
    "font": ("Arial", 10),
    "bg": "#ffffff",
    "fg": "#333333",
    "relief": "solid",
    "borderwidth": 1
}

config_label = {
    "bg": "#f0f0f5",
    "fg": "#333333",
    "font": ("Arial", 11, "bold")
}

config_title = {
    "bg": "#f0f0f5",
    "fg": "#333333",
    "font": ("Arial", 18, "bold")
}

config_radio_button ={
    'bg':"#f0f0f5",
    'fg':"#333333",
    'font':("Arial", 11, "bold"),
    'selectcolor':"#ffffff"
}

class AppCalculadora(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Calculadora Métodos Análiticos")
        self.minsize(width=600, height=400)
        self.geometry("600x400+50+50")
        self.configure(bg="#003F87")

        self.create_notebook()

    def create_notebook(self):

        self.notebook = TabbedBrowser(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.notebook.add_tab(tab_2_factor_crossed, tab_name="Cruzado")
        # self.notebook.add_tab(tab_2_factor_nested, tab_name="Anidado")
        
        self.notebook.pack(expand=True, fill="both")
        
class tab_2_factor_crossed(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configurar_pestaña()

    def configurar_pestaña(self):
        self.title = tk.Label(self, text="ANOVA de 2 Factores Cruzados", **config_title)
        self.title.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.label_nofa = tk.Label(self, text="No. de factores A:", **config_label)
        self.label_nofb = tk.Label(self, text="No. de factores B:", **config_label) 
        self.label_noel = tk.Label(self, text="No. de elementos:", **config_label) 
        self.label_nofa.grid(row=1, column=0, padx=5)
        self.label_nofb.grid(row=2, column=0, padx=5)
        self.label_noel.grid(row=3, column=0, padx=5)
        self.entry_nofa = tk.Entry(self, width=10, **config_entry)
        self.entry_nofb = tk.Entry(self, width=10, **config_entry)
        self.entry_noel = tk.Entry(self, width=10, **config_entry)
        self.entry_nofa.grid(row=1, column=1, padx=5)
        self.entry_nofb.grid(row=2, column=1, padx=5)
        self.entry_noel.grid(row=3, column=1, padx=5)


if __name__ == "__main__":
    appCal = AppCalculadora()
    appCal.mainloop()