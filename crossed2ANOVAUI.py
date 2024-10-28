import tkinter as tk
import styles
import stadistics.addons as add

class tab_2_factor_crossed(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.no_fA = tk.StringVar(value=2)
        self.no_fB = tk.StringVar(value=2)
        self.no_el = tk.StringVar(value=2)
        self.alpha = tk.StringVar(value=0.05)
        self.tags_names = [tk.StringVar() for _ in range(4)]
        self.tags_str = ["FactorA", "FactorB", "Eventos", "alpha"]

        self.table_type = tk.StringVar(value="DosColumnas")

        self.create_frames()
        self.configurar_pestaña()
        self.create_buttons()

    def create_frames(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)

        self.frame_title = tk.Frame(self, background='#E0F7FA')
        self.frame_user_data = tk.Frame(self, background='#E0F7FA')
        self.frame_table = tk.Frame(self, background='#E0F7FA')
        self.frame_anovatable = tk.Frame(self, background='#E0F7FA')
        
        self.frame_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.frame_user_data.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.frame_user_data.grid_columnconfigure(0, weight=1)
        self.frame_user_data.grid_columnconfigure(1, weight=1)
        self.frame_user_data.grid_columnconfigure(2, weight=1)
        self.frame_user_data.grid_columnconfigure(3, weight=1)
        self.frame_user_data.grid_columnconfigure(4, weight=1)

        self.frame_table.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.frame_anovatable.grid(row=3, column=0, columnspan=2, sticky='nsew')

    def configurar_pestaña(self):
        self.title = tk.Label(self.frame_title, text="ANOVA de 2 Factores Cruzados", **styles.config_title, anchor="center")
        self.title.pack(fill='both', expand=True)
        self.label_nofa = tk.Label(self.frame_user_data, text="No. factores A:", **styles.config_label)
        self.label_nofb = tk.Label(self.frame_user_data, text="No. factores B:", **styles.config_label) 
        self.label_noel = tk.Label(self.frame_user_data, text="No. elementos:", **styles.config_label)
        self.label_alpha= tk.Label(self.frame_user_data, text="Alpha:", **styles.config_label) 
        self.label_nofa.grid(row=1, column=0, padx=5, sticky='w')
        self.label_nofb.grid(row=2, column=0, padx=5, sticky='w')
        self.label_noel.grid(row=3, column=0, padx=5, sticky='w')
        self.label_alpha.grid(row=4, column=0, padx=5, sticky='w')
        self.entry_nofa = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_fA, **styles.config_entry)
        self.entry_nofb = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_fB, **styles.config_entry)
        self.entry_noel = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_el, **styles.config_entry)
        self.entry_alpha= tk.Entry(self.frame_user_data, width=5, textvariable=self.alpha, **styles.config_entry)
        self.entry_nofa.grid(row=1, column=1, padx=5, sticky='w')
        self.entry_nofb.grid(row=2, column=1, padx=5, sticky='w')
        self.entry_noel.grid(row=3, column=1, padx=5, sticky='w')
        self.entry_alpha.grid(row=4, column=1, padx=5, sticky='w')
        self.entry_tagfa = tk.Entry(self.frame_user_data, width=14, **styles.config_entry)
        self.entry_tagfb = tk.Entry(self.frame_user_data, width=14, **styles.config_entry)
        self.entry_tagel = tk.Entry(self.frame_user_data, width=14, **styles.config_entry)
        self.entry_tagal = tk.Entry(self.frame_user_data, width=14, **styles.config_entry)
        self.entry_tagfa.grid(row=1, column=2, padx=5, sticky='w')
        self.entry_tagfb.grid(row=2, column=2, padx=5, sticky='w')
        self.entry_tagel.grid(row=3, column=2, padx=5, sticky='w')
        self.entry_tagal.grid(row=4, column=2, padx=5, sticky='w')
        self.entry_tagfa.insert(0,self.tags_str[0])
        self.entry_tagfb.insert(0,self.tags_str[1])
        self.entry_tagel.insert(0,self.tags_str[2])
        self.entry_tagal.insert(0,self.tags_str[3])
    
    def create_buttons(self):
        self.button_calculate = tk.Button(self.frame_user_data, width=12, **styles.config_boton, text="Importar Datos")
        self.button_calculate.grid(row=1, column=5, padx=5, pady=10,sticky='w')

        self.radiob_cxrc = tk.Radiobutton(self.frame_user_data, text="FilxCol. C.", value="FilaxColumnaC.", variable=self.table_type, **styles.config_radio_button)
        self.radiob_cxr = tk.Radiobutton(self.frame_user_data, text="FilaxCol.", value="FilaxColumna", variable=self.table_type, **styles.config_radio_button)
        self.radiob_cc = tk.Radiobutton(self.frame_user_data, text="3Columnas", value="DosColumnas", variable=self.table_type, **styles.config_radio_button)
        self.button_calculate = tk.Button(self.frame_user_data, width=12, text="Calcular tabla", **styles.config_boton)
        self.radiob_cxrc.grid(row=2, column=5, padx=5, pady=10, sticky='w')
        self.radiob_cxr.grid(row=3, column=5, padx=5, pady=10, sticky='w')
        self.radiob_cc.grid(row=4, column=5, padx=5, pady=10, sticky='w')
        self.button_calculate.grid(row=5, column=5, padx=5, pady=10, sticky='w')

        self.button_add_row = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton)
        self.button_remove_row = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton)
        self.button_add_col = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton)
        self.button_remove_col = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton)
        self.button_add_elem = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton)
        self.button_remove_elem = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton)
        
        self.button_add_row.grid(row=1, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_row.grid(row=1, column=4, padx=5, pady=10, sticky='w')
        self.button_add_col.grid(row=2, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_col.grid(row=2, column=4, padx=5, pady=10, sticky='w')
        self.button_add_elem.grid(row=3, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_elem.grid(row=3, column=4, padx=5, pady=10, sticky='w')
    

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=600, height=400)
    root.geometry("600x400+50+50")
    frame = tab_2_factor_crossed(root)
    frame.pack(fill='both', expand=1)
    
    root.mainloop()