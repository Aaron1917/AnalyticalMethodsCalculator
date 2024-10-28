import tkinter as tk
from tkinter import ttk
from navigation_tab import TabbedBrowser
from crossed2ANOVAUI import tab_2_factor_crossed
import styles

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


if __name__ == "__main__":
    appCal = AppCalculadora()
    appCal.mainloop()