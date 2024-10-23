import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scipy.stats as stats
import tkinter as tk
from tkinter import filedialog, messagebox
from stadistics.anova2factors import anova2f as ava2
from stadistics.anova2factors import custom_round as cr

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi Aplicación")
        self.minsize(width=1280, height=720)
        self.geometry("1280x720")
        
        self.tags = ["FactorA", "FactorB", "Eventos", "alpha"] # analista, dia
        self.coloum_title = ["Total", "Between", "Factor A", "Factor B", "Interacción", "Error"]
        self.row_title = ["Factor de variación", "Suma de Cuadrados", "Grados de libertad", "Media de cuadrados", "F. Calculada", "F. tablas"]

        self.factorA = tk.StringVar()
        self.factorB = tk.StringVar()
        self.no_group = tk.StringVar()
        self.alpha = tk.StringVar(value=0.05)
        self.tags_names = [tk.StringVar() for _ in range(4)]

        self.matriz_entry = []
        self.fig = None
        self.canvas = None
        self.anova2f = None

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.main_frame = tk.Frame(self, bg="pink")
        self.main_frame.pack(fill='both', expand=True)
        
        self.main_frame.columnconfigure(0, minsize=640, weight=1)
        self.main_frame.columnconfigure(1, minsize=640, weight=1)

        self.main_frame.rowconfigure(0, minsize=200, weight=2)#200
        self.main_frame.rowconfigure(1, minsize=300, weight=3) #320
        self.main_frame.rowconfigure(2, minsize=220, weight=0) # 200
        
        self.entry_frame = tk.Frame(self.main_frame, bg='pale green')
        self.entry_frame.grid(row=0, column=0, sticky='nsew')
        
        self.data_frame = tk.Frame(self.main_frame, bg='light blue')
        self.data_frame.grid(row=1, column=0, sticky='nsew')

        self.result_frame = tk.Frame(self.main_frame, bg='coral')
        self.result_frame.grid(row=2, column=0, sticky='nsew')

        self.figure_frame1 = tk.Frame(self.main_frame, bg='light goldenrod')
        self.figure_frame1.grid(row=0, column=1,sticky='nsew')

        self.figure_frame2 = tk.Frame(self.main_frame, bg='plum2')
        self.figure_frame2.grid(row=1, column=1, rowspan=2, sticky='nsew')

    def create_widgets(self):
        self.create_factor_entries()
        self.create_buttons()
        self.create_canvas_frames()
        self.create_scrollbars()
        self.create_result_table()
        self.calculate_anova2f(True)

    def create_factor_entries(self):

        tk.Label(self.entry_frame, text="No. grupos factor A:").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.number_factorA = tk.Entry(self.entry_frame, textvariable=self.factorA, width=5)
        self.number_factorA.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.name_factorA = self.create_factor_name_entry(0, 2)

        tk.Label(self.entry_frame, text="No. grupos factor B:").grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.number_factorB = tk.Entry(self.entry_frame, textvariable=self.factorB, width=5)
        self.number_factorB.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.name_factorB = self.create_factor_name_entry(1, 2)

        tk.Label(self.entry_frame, text="No. valores por grupo:").grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.values_group = tk.Entry(self.entry_frame, textvariable=self.no_group, width=5)
        self.values_group.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.name_factorC = self.create_factor_name_entry(2, 2)

        tk.Label(self.entry_frame, text="Significancia:").grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.alpha_entry = tk.Entry(self.entry_frame, textvariable=self.alpha, width=5)
        self.alpha_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        self.name_alpha = self.create_factor_name_entry(3, 2)
    
    def create_factor_name_entry(self, row: int, column: int):
        entry = tk.Entry(self.entry_frame, textvariable=self.tags_names[row], width=10)
        entry.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        entry.insert(0, self.tags[row])
        return entry
    
    def create_buttons(self):
        tk.Button(self.entry_frame, text="Crear Tabla", command=self.create_table, width=12).grid(row=0, column=3, pady=10, padx=10, sticky='nsew')
        tk.Button(self.entry_frame, text="Calcular", command=self.calculate_anova2f, width=12).grid(row=2, column=3, pady=10, padx=10, sticky='nsew')
        tk.Button(self.entry_frame, text='Importar Datos', command=self.import_data, width=12).grid(row =1, column=3, pady=10, padx=10, sticky='nsew')

    def create_canvas_frames(self, row_: int =0, column_: int =0):
        # Configuración de columnas
        self.data_frame.columnconfigure(0, minsize=70, weight=0)  # Columna fija de 100
        self.data_frame.columnconfigure(1, weight=1)  # Columna que se expande
        self.data_frame.columnconfigure(2, weight=1)  # Columna que se expande
        self.data_frame.columnconfigure(3, weight=1)  # Columna que se expande
        self.data_frame.columnconfigure(4, minsize=10, weight=0)  # Columna para scroll bar

        # Configuración de filas
        self.data_frame.rowconfigure(0, minsize=30, weight=0)  # Fila fija de 30
        self.data_frame.rowconfigure(1, weight=1)  # Fila que se expande
        self.data_frame.rowconfigure(2, weight=1)  # Fila que se expande
        self.data_frame.rowconfigure(3, minsize=10 ,weight=0)  # Fila para scroll bar

        # Frame para la tabla de entrada
        self.canvas_top_left = tk.Frame(self.data_frame, bg='deep pink2', width=70, height=30)
        self.canvas_top_left.grid(row=row_, column=column_, sticky='nsew')

        self.canvas_top_right = tk.Canvas(self.data_frame, bg='pink', height=30)
        self.canvas_top_right.grid(row=row_, column=column_ + 1, columnspan=3, sticky="nsew")

        self.canvas_bottom_left = tk.Canvas(self.data_frame, bg='pale green', width=70)# coloque span = 2 = 0
        self.canvas_bottom_left.grid(row=row_ + 1, column=column_, rowspan=2, sticky="nsew")

        self.canvas_bottom_right = tk.Canvas(self.data_frame, bg='red')
        self.canvas_bottom_right.grid(row=row_ + 1, column=column_ + 1, rowspan=2, columnspan=3, sticky="nsew")

        # Crear marcos en los canvas
        self.canvas_top_right_frame = tk.Frame(self.canvas_top_right)
        self.canvas_top_right.create_window((0, 0), window=self.canvas_top_right_frame, anchor="nw")

        self.canvas_bottom_left_frame = tk.Frame(self.canvas_bottom_left)
        self.canvas_bottom_left.create_window((0, 0), window=self.canvas_bottom_left_frame, anchor="nw")

        self.canvas_bottom_right_frame = tk.Frame(self.canvas_bottom_right)
        self.canvas_bottom_right.create_window((0, 0), window=self.canvas_bottom_right_frame, anchor="nw")

    def create_scrollbars(self, row_ = 1, columnx_ = 1, column_y = 4):
        # Scrollbars para los canvas
        scrollbar_y = tk.Scrollbar(self.data_frame, orient="vertical", command=self.canvas_bottom_right.yview)
        scrollbar_y.grid(row=row_, column=column_y, rowspan=2, sticky="ns")

        scrollbar_x = tk.Scrollbar(self.data_frame, orient="horizontal", command=self.canvas_bottom_right.xview)
        scrollbar_x.grid(row=row_ + 2, column=columnx_, columnspan=3, sticky="ew")

        self.canvas_bottom_right.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sincronización de desplazamiento
        self.canvas_bottom_right.config(yscrollcommand=lambda *args: [scrollbar_y.set(*args), self.sync_scroll_y(*args)])
        self.canvas_bottom_left.config(yscrollcommand=self.sync_scroll_y)
        self.canvas_bottom_right.config(xscrollcommand=lambda *args: [scrollbar_x.set(*args), self.sync_scroll_x(*args)])
        self.canvas_top_right.config(xscrollcommand=self.sync_scroll_x)
    
    def sync_scroll_y(self, *args):
        self.canvas_bottom_right.yview_moveto(args[0])
        self.canvas_bottom_left.yview_moveto(args[0])

    def sync_scroll_x(self, *args):
        self.canvas_bottom_right.xview_moveto(args[0])
        self.canvas_top_right.xview_moveto(args[0])

    def clear_canvas(self, canvas_frame):
        for widget in canvas_frame.winfo_children():
            widget.destroy()

    def update_scrollregions(self):
        self.canvas_bottom_right_frame.update_idletasks()
        self.canvas_bottom_right.config(scrollregion=self.canvas_bottom_right.bbox("all"))
        self.canvas_top_right_frame.update_idletasks()
        self.canvas_top_right.config(scrollregion=self.canvas_top_right.bbox("all"))
        self.canvas_bottom_left_frame.update_idletasks()
        self.canvas_bottom_left.config(scrollregion=self.canvas_bottom_left.bbox("all"))

    def create_table(self):
        p, q, r  = self.numbers_group()
        if p < 2 or q < 2:
            messagebox.showinfo("Error", "Numero de factores A o B tiene que ser mayor a 1")
            return

         # Limpiar los widgets existentes en los frames de los canvas
        self.clear_canvas(self.canvas_top_right_frame)
        self.clear_canvas(self.canvas_bottom_left_frame)
        self.clear_canvas(self.canvas_bottom_right_frame)

        for i in range(p+1): # columns
            factorA = []
            for j in range(q+1): # rows
                factorB = []
                for k in range(r): # row of rows
                    entrada = self.create_table_entry(i, j, k, r)
                    if entrada != None:
                        factorB.append(entrada)
                factorA.append(factorB) # if j > 0
            self.matriz_entry.append(factorA) # if i >0
        self.update_scrollregions()

    def create_table_entry(self, i: int, j: int, k: int, r: int):
        if i == 0 and j == 0:
            entrada = tk.Entry(self.canvas_top_left, width=10)
            entrada.grid(row=j, column=i, padx=5, pady=5)
            entrada.insert(0, "Factor")
            entrada.config(state="readonly")
            # return None
        elif i == 0: # column 0
            entrada = tk.Entry(self.canvas_bottom_left_frame, width=10)
            entrada.grid(row=(j-1)*r+k+1, column=i, padx=5, pady=5)
            entrada.insert(0, f"{self.tags_names[1].get()} {j}") if k == 0 else entrada.insert(0, "")
            entrada.config(state="readonly")
            #return None
        elif j == 0:# row 0
            entrada = tk.Entry(self.canvas_top_right_frame, width=10)
            entrada.grid(row=j, column=i, padx=5, pady=5)
            entrada.insert(0, f"{self.tags_names[0].get()} {i}") 
            entrada.config(state="readonly")
            #return None
        elif j > 0 and i > 0:
            entrada = tk.Entry(self.canvas_bottom_right_frame, width=10)
            entrada.grid(row=(j-1)*r+k+1, column=i, padx=5, pady=5)
            # entrada.insert(0, 0)
        return entrada

    def create_result_table(self, row_= 0, column_=0):

        self.result_frame.columnconfigure(0, minsize=100, weight=0)  # Columna fija de 630
        self.result_frame.columnconfigure(1, minsize=520, weight=1)  # Columna fija de 630
        #self.result_frame.columnconfigure(2, minsize=10, weight=0)  # Columna para scroll bar #4

        # Configuración de filas
        self.result_frame.rowconfigure(0, minsize=8, weight=0)  # Fila fija de 30
        self.result_frame.rowconfigure(1, minsize=198, weight=0)
        self.result_frame.rowconfigure(2, minsize=12, weight=0)  # Fila para scroll bar #3

        self.canvas_result = tk.Canvas(self.result_frame, bg='orange2', height=202) #  bg='light blue'
        #scrollbar_y_result = tk.Scrollbar(self.result_frame, orient="vertical", command=self.canvas_result.yview)
        scrollbar_x_result = tk.Scrollbar(self.result_frame, orient="horizontal", command=self.canvas_result.xview)
        self.table_frame_result = tk.Frame(self.canvas_result, height=120)

        self.table_frame_result.bind("<Configure>", lambda e: self.canvas_result.configure(scrollregion=self.canvas_result.bbox("all")))

        self.canvas_result.create_window((0, 0), window=self.table_frame_result, anchor="nw")
        self.canvas_result.grid(row=row_, column=column_, rowspan=2, columnspan=2, sticky="nsew") # , padx=5, pady=5
        #scrollbar_y_result.grid(row=row_, column=column_+2, rowspan=2, sticky="ns")
        scrollbar_x_result.grid(row=row_ + 2, column=column_, columnspan=2, sticky="ew")
        self.canvas_result.configure(xscrollcommand=scrollbar_x_result.set) #yscrollcommand=scrollbar_y_result.set

    def calculate_anova2f(self, initialize = False):
        if initialize:
            self.display_results(None, 20)
            return None
        p , q, r = self.numbers_group()
        entradas = self.get_values_entry()

        self.anova2f = ava2(n_factorA=p, n_factorB=q, n_elements=r, data=entradas, alpha=float(self.alpha.get()))
        self.anova2f.set_alpha(float(self.alpha.get()))
        self.display_results(self.anova2f)
        self.delete_plot()
        self.plot_distribution_f(0, 0)

    def numbers_group(self):
        p = int(self.factorA.get())  # column
        q = int(self.factorB.get())  # row
        r = int(self.no_group.get())  # intern row
        return p,q,r

    def get_values_entry(self):
        p, q, r = self.numbers_group()
        entradas = []
        for i in range(1,p+1):
            factorA = []
            for j in range(1,q+1):
                factorB = []
                for k in range(r):
                    if i>0 and j>0:
                        factorB.append(float(self.matriz_entry[i][j][k].get()))
                factorA.append(factorB)
            entradas.append(factorA)
        print(entradas)
        return entradas

    def display_results(self, ava2f: ava2, width: int = 20):
        for i in range(len(self.row_title) + 1):
            for j in range(len(self.coloum_title)):
                entrada = tk.Entry(self.table_frame_result, width=width)
                entrada.grid(row=i, column=j, padx=5, pady=5)
                if i == 0:
                    entrada.insert(0, self.row_title[j])
                elif j == 0:
                    entrada.insert(0, self.coloum_title[i - 1])
                else:
                    entrada.insert(0,"") if ava2f == None else entrada.insert(0, ava2f.table_results_round[i - 1][j - 1])
                entrada.config(state='readonly')

    def plot_distribution_f(self, index:int=0, two_tails: bool = False, row: int = 0, column: int  = 0):
        self.delete_plot()

        dfn = self.anova2f.DF_list[index]
        dfd = self.anova2f.df_err
        alpha = float(self.alpha.get())
        f_cal = self.anova2f.f_calculated[index]

        # Calcular los valores críticos de F para ambas colas
        f_critica_izquierda = stats.f.ppf(alpha, dfn, dfd) if two_tails else 0.0
        f_critica_derecha = stats.f.ppf(1 - alpha, dfn, dfd)

        max_x = round(f_critica_derecha*1.15)
        # Generar valores de la distribución F
        x = np.linspace(0, max_x, 1000)
        y = stats.f.pdf(x, dfn, dfd)

        # Crear la figura y el gráfico
        self.fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, label='Distribución F de Fisher', color='blue')

        if two_tails:
            # Rellenar la zona de rechazo por la cola izquierda
            # ax.fill_between(x, y, where=(x <= f_critica_izquierda), color='red', alpha=0.5, label='Zona de rechazo (cola izquierda)')
            plt.axvline(f_critica_izquierda, color='red', linestyle='--', label=f'F de rechazo izquierda = {cr(f_critica_izquierda)}')

        # Rellenar la zona de rechazo por la cola derecha
        # ax.fill_between(x, y, where=(x >= f_critica_derecha), color='red', alpha=0.5, label='Zona de rechazo (cola derecha)')
        plt.axvline(f_critica_derecha, color='red', linestyle='--', label=f'F de rechazo derecha = {cr(f_critica_derecha)}')

        # Marcar el valor de F calculado
        ax.axvline(f_cal, color='green', linestyle='--', label=f'F calculada = {cr(f_cal)}')

        # Configurar etiquetas y título
        ax.set_title('Distribución F de Fisher y Zonas de Rechazo')
        ax.set_xlabel('Valores de F')
        ax.set_ylabel('Densidad de probabilidad')
        ax.legend()

        # Crear el widget de Matplotlib para Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.figure_frame2)
        self.canvas.draw()

        # Ubicar el widget en la celda especificada (row=4, column=6)
        self.canvas.get_tk_widget().grid(row=row, column=column, rowspan=5, columnspan=4)
    
    def delete_plot(self):
        # Limpiar la figura actual si existe
        if self.canvas is not None:
            self.canvas.get_tk_widget().grid_forget()  # Eliminar el widget de la cuadrícula
            self.canvas = None
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None

    def import_data(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
        )
        if archivo:
            try:
                p,q,r=self.numbers_group()
                self.copiar_datos_excel(archivo, row=(q*r)+1, column=p+1)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def copiar_datos_excel(self, archivo, row: int=5, column: int=3):
        df = pd.read_excel(archivo)
        df = df.fillna(0)
        df_copiado = df.iloc[:row, :column]

        lista_de_listas = df_copiado.values.tolist()
        encabezados = df_copiado.columns.tolist()
        lista_de_listas.insert(0, encabezados)
        # print("Datos copiados:")
        # print(lista_de_listas)
        self.copy_table_entry(lista_de_listas)
        messagebox.showinfo("Éxito", "Los datos se importaron correctamente.")

    def copy_table_entry(self, data: list):
        p, q, r =self.numbers_group()
        for i in range(p+1):
            for j in range(q+1):
                for k in range(r):
                    self.matriz_entry[i][j][k].insert(0,data[(j-1)*r+k+1][i])

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
