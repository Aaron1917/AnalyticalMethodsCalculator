import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from table_treeview import EditableTreeviewGadget as table
import styles
import stadistics.addons as addons
from stadistics.two_factor_nested_ANOVA import Nested2FactorAnava as N2FA

class tab_2_factor_nested(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.no_fA = tk.StringVar(value=2)
        self.no_fB = tk.StringVar(value=2)
        self.no_el = tk.StringVar(value=2)
        self.alpha = tk.StringVar(value=0.05)
        self.tags_str = ["FactorA", "FactorB", "Eventos", "alpha"]
        self.tags_names = [tk.StringVar(value=self.tags_str[_]) for _ in range(4)]

        self.table_type = tk.StringVar(value="TresColumnas")
        self.current_table_type = 'TresColumnas'

        self.create_frames()
        self.configurar_pestaña()
        self.create_buttons()
        self.input_data = None
        self.anova_data = None
        self.input_data_widget = None
        self.anova_data_widget = None

        self.input_data_widget = table(parent=self.frame_table,
                                       dataframe=self.input_data,
                                       num_visible_rows=26)
        self.input_data_widget.pack(expand=True, fill='both')

        self.anova_data_widget = table(parent=self.frame_anovatable,
                                       dataframe=self.anova_data,
                                       num_visible_rows=4,
                                       min_width_cell=240,
                                       editable=False)
        self.anova_data_widget.pack(expand=True, fill='both')

        self.clear_data_table()
        self.clear_anova_table()

    def create_frames(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

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
        self.title = tk.Label(self.frame_title, text="ANOVA de 2 Factores Anidados", **styles.config_title, anchor="center")
        self.title.pack(fill='both', expand=True)
        self.label_nofa = tk.Label(self.frame_user_data, text="No. factores A:", **styles.config_label)
        self.label_nofb = tk.Label(self.frame_user_data, text="No. factores B:", **styles.config_label) 
        self.label_noel = tk.Label(self.frame_user_data, text="No. elementos:", **styles.config_label)
        self.label_alpha= tk.Label(self.frame_user_data, text="Alpha:", **styles.config_label) 
        self.label_nofa.grid(row=1, column=0, padx=5, sticky='w')
        self.label_nofb.grid(row=2, column=0, padx=5, sticky='w')
        self.label_noel.grid(row=3, column=0, padx=5, sticky='w')
        self.label_alpha.grid(row=4, column=0, padx=5, sticky='w')
        self.entry_nofa = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_fA, state='readonly',**styles.config_entry,)
        self.entry_nofb = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_fB, state='readonly', **styles.config_entry)
        self.entry_noel = tk.Entry(self.frame_user_data, width=5, textvariable=self.no_el, state='readonly', **styles.config_entry)
        self.entry_alpha= tk.Entry(self.frame_user_data, width=5, textvariable=self.alpha, **styles.config_entry)
        self.entry_nofa.grid(row=1, column=1, padx=5, sticky='w')
        self.entry_nofb.grid(row=2, column=1, padx=5, sticky='w')
        self.entry_noel.grid(row=3, column=1, padx=5, sticky='w')
        self.entry_alpha.grid(row=4, column=1, padx=5, sticky='w')
        self.entry_tagfa = tk.Entry(self.frame_user_data, width=14, textvariable=self.tags_names[0], **styles.config_entry)
        self.entry_tagfb = tk.Entry(self.frame_user_data, width=14, textvariable=self.tags_names[1], **styles.config_entry)
        self.entry_tagel = tk.Entry(self.frame_user_data, width=14, textvariable=self.tags_names[2], **styles.config_entry)
        self.entry_tagal = tk.Entry(self.frame_user_data, width=14, textvariable=self.tags_names[3], **styles.config_entry)
        self.entry_tagfa.grid(row=1, column=2, padx=5, sticky='w')
        self.entry_tagfb.grid(row=2, column=2, padx=5, sticky='w')
        self.entry_tagel.grid(row=3, column=2, padx=5, sticky='w')
        self.entry_tagal.grid(row=4, column=2, padx=5, sticky='w')
    
    def create_buttons(self):
        self.radiob_cxrc = tk.Radiobutton(self.frame_user_data, text="FilxCol. C.", value="FilaxColumnaC.", variable=self.table_type, **styles.config_radio_button, command=self.change_table_type)
        self.radiob_cxr = tk.Radiobutton(self.frame_user_data, text="FilaxCol.", value="FilaxColumna", variable=self.table_type, **styles.config_radio_button, command=self.change_table_type)
        self.radiob_cc = tk.Radiobutton(self.frame_user_data, text="3Columnas", value="TresColumnas", variable=self.table_type, **styles.config_radio_button, command=self.change_table_type)
        self.button_calculate = tk.Button(self.frame_user_data, width=12, text="Calcular tabla", command=self.calcular_anova,**styles.config_boton)
        self.button_import = tk.Button(self.frame_user_data, width=12, text="Importar Datos", command=self.import_data, **styles.config_boton)
        self.button_update_table = tk.Button(self.frame_user_data, width=12, text="Actualizar tabla", **styles.config_boton)
        self.button_clear_table = tk.Button(self.frame_user_data, width=12, text="Limpiar tabla", command=self.clear_data_table, **styles.config_boton)

        self.radiob_cxrc.grid(row=2, column=5, padx=5, pady=10, sticky='w')
        self.radiob_cxr.grid(row=3, column=5, padx=5, pady=10, sticky='w')
        self.radiob_cc.grid(row=4, column=5, padx=5, pady=10, sticky='w')
        self.button_calculate.grid(row=5, column=0, padx=5, pady=10, sticky='w')
        self.button_import.grid(row=5, column=5, padx=5, pady=10, sticky='w')
        self.button_update_table.grid(row=1, column=5, padx=5, pady=10, sticky='w')
        self.button_clear_table.grid(row=5, column=1, padx=5, pady=10, sticky='w')

        self.button_add_row = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton, command=self.add_fa_fun)
        self.button_remove_row = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton, command=self.rem_fa_fun)
        self.button_add_col = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton, command=self.add_fb_fun)
        self.button_remove_col = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton, command=self.rem_fb_fun)
        self.button_add_elem = tk.Button(self.frame_user_data, width=8, text="Añadir", **styles.config_boton, command=self.add_el_fun)
        self.button_remove_elem = tk.Button(self.frame_user_data, width=8, text="Remover", **styles.config_boton, command=self.rem_el_fun)
        
        self.button_add_row.grid(row=1, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_row.grid(row=1, column=4, padx=5, pady=10, sticky='w')
        self.button_add_col.grid(row=2, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_col.grid(row=2, column=4, padx=5, pady=10, sticky='w')
        self.button_add_elem.grid(row=3, column=3, padx=5, pady=10, sticky='w')
        self.button_remove_elem.grid(row=3, column=4, padx=5, pady=10, sticky='w')

    def add_fa_fun(self):
        self.no_fA.set(int(self.no_fA.get())+1)
        self.change_table_type('FilaxColumna')
        datos = [np.nan]*self.input_data.shape[0]
        self.input_data[f'{self.tags_names[0].get()} {int(self.no_fA.get())}'] = datos
        #print(f"los factores al ejecutar son: \n{self.input_data}")
        self.input_data_widget.set_parameter(dataframe=self.input_data)
        self.change_table_type()

    def rem_fa_fun(self):
        num = int(self.no_fA.get())-1
        if num < 2:
            self.no_fA.set(2) 
        else:
            self.no_fA.set(num)
            self.change_table_type('FilaxColumna')
            self.input_data = self.input_data.drop(f'{self.tags_names[0].get()} {num+1}', axis=1)
            self.input_data_widget.set_parameter(dataframe=self.input_data)
            self.change_table_type()

    def add_fb_fun(self):
        self.no_fB.set(int(self.no_fB.get())+1)
        self.change_table_type('FilaxColumnaC.')
        p,q,r = self.numbers_group()
        datos = [np.nan]*r
        dato_str = ', '.join(map(str, datos))
        lista_datos = [dato_str for a in range(p)]
        lista_datos.insert(0, f'{self.tags_names[1].get()} {q}')
        self.input_data.loc[len(self.input_data)] = lista_datos
        self.input_data_widget.set_parameter(dataframe=self.input_data)
        self.change_table_type()

    def rem_fb_fun(self):
        num = int(self.no_fB.get())-1
        if num < 2:
            self.no_fB.set(2) 
        else:
            self.no_fB.set(num)
            self.change_table_type('FilaxColumnaC.')
            self.input_data = self.input_data.drop(num)
            self.input_data_widget.set_parameter(dataframe=self.input_data)
            self.change_table_type()

    def add_el_fun(self):
        self.no_el.set(int(self.no_el.get())+1)
        self.change_table_type('FilaxColumnaC.')
        name_col = self.input_data.columns.to_list()[1:]
        for col in name_col:
            self.input_data[col] = self.input_data[col].apply(lambda x: x + ', ' + str(np.nan))
        self.input_data_widget.set_parameter(dataframe=self.input_data)
        self.change_table_type()

    def rem_el_fun(self):
        num = int(self.no_el.get())-1
        if num < 2:
            self.no_el.set(2)
        else:
            self.no_el.set(num)
            self.change_table_type('FilaxColumnaC.')
            name_col = self.input_data.columns.to_list()[1:]
            for col in name_col:
                self.input_data[col] = self.input_data[col].apply(lambda x: ', '.join(x.split(', ')[:-1]))
            self.input_data_widget.set_parameter(dataframe=self.input_data)
            self.change_table_type()
    
    def numbers_group(self):
        p = int(self.no_fA.get())
        q = int(self.no_fB.get())
        r = int(self.no_el.get())
        return p,q,r
    
    def clear_data_table(self):
        p, q, r = self.numbers_group()
        
        if self.table_type.get() == "TresColumnas":
            list_table = []
            for a in range(p):
                for b in range(q):
                    for e in range(r):
                        list_table.append({
                            self.tags_names[0].get():f"{self.tags_names[0].get()} {a + 1}",
                            self.tags_names[1].get():f"{self.tags_names[1].get()} {b + 1}",
                            self.tags_names[2].get():np.nan})
            self.input_data = pd.DataFrame(list_table)
        elif self.table_type.get() == "FilaxColumna":
            headers = [f"{self.tags_names[0].get()} {a + 1}" for a in range(p)]
            headers.insert(0,'Factores')
            filas = [f"{self.tags_names[1].get()} {b + 1}"
                     for b in range(q)
                     for e in range(r)]
            self.input_data = pd.DataFrame(filas, columns=[headers[0]])
            for header in headers[1:]:
                self.input_data[header] = np.nan
        elif self.table_type.get() == "FilaxColumnaC.":
            headers = [f"{self.tags_names[0].get()} {a + 1}" for a in range(p)]
            headers.insert(0,'Factores')
            filas = [f"{self.tags_names[1].get()} {b + 1}"
                     for b in range(q)]
            self.input_data = pd.DataFrame(filas, columns=[headers[0]])
            dato = [np.nan] * r
            dato_str = ', '.join(map(str, dato))
            for header in headers[1:]:
                self.input_data[header] = dato_str
        #print(self.input_data)
        self.input_data_widget.set_parameter(dataframe=self.input_data)

    def change_table_type(self, target_table_type: str = None):
        if target_table_type is None:
            target_table_type = self.table_type.get()
        # print(f"\nEl valor actual {self.current_table_type} pasa a: {target_table_type}")
        if self.current_table_type == target_table_type:
            self.input_data = self.input_data_widget.get_dataframe()
            self.input_data_widget.set_parameter(dataframe=self.input_data)
            return None
        self.input_data = self.input_data_widget.get_dataframe()
        while True:
            if self.current_table_type == 'TresColumnas':
                self.input_data = addons.convert_ThreeCol2RxCc(self.input_data)
                self.current_table_type = 'FilaxColumnaC.'
            elif self.current_table_type == 'FilaxColumnaC.':
                self.input_data = addons.convert_RxCc2RxC(self.input_data)
                self.current_table_type = 'FilaxColumna'
            elif self.current_table_type == 'FilaxColumna':
                self.input_data = addons.convert_RxC2ThreeCol(self.input_data,
                                                              self.tags_names[0].get(),
                                                              self.tags_names[1].get(),
                                                              self.tags_names[2].get())
                self.current_table_type = 'TresColumnas'
            if self.current_table_type == target_table_type:
                self.input_data_widget.set_parameter(dataframe=self.input_data)
                break

    def import_data(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
        )
        if archivo:
            try:
                self.copiar_datos_excel(archivo)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def copiar_datos_excel(self, archivo):
        p,q,r=self.numbers_group()
        table_type = self.table_type.get()
        if table_type == "TresColumnas":
            column = 3
            row = 1 + (p * q * r)
        elif table_type == "FilaxColumna":
            column = p + 1
            row = 1 + (q * r)
        elif table_type == "FilaxColumnaC.":
            column = p + 1
            row = 1 + q

        df = pd.read_excel(archivo)
        self.input_data = df.iloc[:row, :column]
        if table_type == 'FilaxColumna':
            col_names = self.input_data.columns.to_list()
            self.input_data[col_names[0]] = self.input_data[col_names[0]].ffill()
        elif table_type == 'TresColumnas':
            col_names = self.input_data.columns.to_list()
            self.input_data[col_names[0]] = self.input_data[col_names[0]].ffill()
            self.input_data[col_names[1]] = self.input_data[col_names[1]].ffill()
        self.input_data_widget.set_parameter(dataframe=self.input_data)
        
        messagebox.showinfo("Éxito", "Los datos se importaron correctamente.")

    def calcular_anova(self):
        self.input_data = self.input_data_widget.get_dataframe()
        self.input_data.replace('nan', np.nan, inplace=True)
        if self.input_data.isna().any().any():
            messagebox.showerror("Error", "Alguno de los elementos en la tabla no es válido")
            self.change_table_type()
            return None
        
        self.change_table_type("TresColumnas")
        col3 = self.input_data.columns.to_list()[2]
        self.input_data[col3] = pd.to_numeric(self.input_data[col3], errors='coerce')
        if self.input_data[col3].isnull().any():
            messagebox.showerror("Error", "Alguno de los elementos en la tabla no es válido")
            self.change_table_type()
            return None
        
        p, q, r = self.numbers_group()
        if p * q * r != self.input_data.shape[0]:
            messagebox.showerror("Error", "El número de datos no coincide con los parámetros")
            return None
        self.c2fa = N2FA(data=self.input_data, alpha=float(self.alpha.get()))
        self.change_table_type()
        self.anova_data = pd.DataFrame(self.c2fa.calculate_anova_table())
        self.anova_data = addons.apply_funtion_df(self.anova_data, addons.custom_round)
        self.anova_data_widget.set_parameter(dataframe=self.anova_data)
    
    def clear_anova_table(self):
        self.anova_data = pd.DataFrame({
            'Factor de Variación': ['Total', self.tags_names[0].get(), self.tags_names[1].get(), 'Error'],
            'Suma de cuadrados ': ['' for _ in range(4)],
            'Grados de libertad': ['' for _ in range(4)],
            'Media de cuadrados': ['' for _ in range(4)],
            'F. Calculada': ['' for _ in range(4)]
        })
        self.anova_data_widget.set_parameter(self.anova_data)

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=620, height=700)
    root.geometry("620x700+50+50")
    frame = tab_2_factor_nested(root)
    frame.pack(fill='both', expand=1)
    
    root.mainloop()