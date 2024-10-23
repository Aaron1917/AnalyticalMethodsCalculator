# https://datatab.es/tutorial/two-factorial-anova-without-repeated-measures
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# factores cruzados, factores anidados

class anova2f:

    def __init__(self, n_factorA: int, n_factorB: int, n_elements: int, data: list, alpha: float=0.05):
        self.n_factorA = n_factorA
        self.n_factorB = n_factorB
        self.n_elements = n_elements
        self.data = data.copy()
        self.alpha = alpha
        self.fig = None


    def set_alpha(self, alpha: float):
        self.alpha = alpha
        self.results()

    def mean_tables(self):
        self.group_means = [[sum(sublista) / len(sublista) for sublista in fila] for fila in self.data]
        self.group_mean_factorA = [sum(row) / len(row) for row in self.group_means]
        self.group_mean_factorB = [sum(col) / len(col) for col in zip(*self.group_means)] 
        self.general_mean = sum(self.group_mean_factorA) / len(self.group_mean_factorA)  
        #self.group_means = [[sum(sublista) / len(sublista) for sublista in fila] for fila in self.data]

    #-------------- Square Sum (S.S.)
    def SS_Total(self):
        self.ss_tot = sum((self.data[i][j][k] - self.general_mean) ** 2
                        for i in range(self.n_factorA)
                        for j in range(self.n_factorB)
                        for k in range(self.n_elements))

    def SS_btw(self):
        filas = len(self.group_means)
        columnas = len(self.group_means[0])

        sumatoria = sum((self.group_means[i][j] - self.general_mean) ** 2
                    for i in range(filas)
                    for j in range(columnas))
    
        self.ss_btw = self.n_elements * sumatoria

    def SS_A(self):
        num_grupos = len(self.group_mean_factorA)
    
        sumatoria = sum((self.group_mean_factorA[i] - self.general_mean) ** 2
                        for i in range(num_grupos))
    
        self.ss_fA = self.n_elements * self.n_factorB * sumatoria

    def SS_B(self):
        num_grupos = len(self.group_mean_factorB)
    
        sumatoria = sum((self.group_mean_factorB[i] - self.general_mean) ** 2
                        for i in range(num_grupos))
    
        self.ss_fB = self.n_elements * self.n_factorA * sumatoria

    def SS_AB(self):
        self.ss_AB = self.ss_btw - self.ss_fA - self.ss_fB
    
    def SS_error(self):
        self.ss_err = sum((self.data[i][j][k] - self.group_means[i][j]) ** 2
                        for i in range(self.n_factorA)
                        for j in range(self.n_factorB)
                        for k in range(self.n_elements))
    def calculate_SS(self):
        self.SS_Total()
        self.SS_btw()
        self.SS_A()
        self.SS_B()
        self.SS_AB()
        self.SS_error()

    # --------------- degrades of freedom (d.f.)
    def DF_Total(self):
        self.df_tot = self.n_factorA * self.n_factorB * self.n_elements - 1
    
    def DF_btw(self):
        self.df_btw = self.n_factorA * self.n_factorB - 1

    def DF_factorA(self):
        self.df_fA = self.n_factorA -1

    def DF_factorB(self):
        self.df_fB = self.n_factorB -1

    def DF_AB(self):
        self.df_AB = self.df_fA * self.df_fB
    
    def DF_error(self):
        self.df_err = self.n_factorA * self.n_factorB * (self.n_elements - 1)

    def calculate_DF(self):
        self.DF_Total()
        self.DF_btw()
        self.DF_factorA()
        self.DF_factorB()
        self.DF_AB()
        self.DF_error()
        self.DF_list = [self.df_fA, self.df_fB, self.df_AB]
    #-----------------------------------
    def results(self):
        self.mean_tables()

        self.calculate_SS()
        self.calculate_DF()

        self.varianz()
        self.f_fisher()
        self.create_table()

    def varianz(self):
        self.varianz_table = [self.ss_tot/self.df_tot,
                              self.ss_btw/self.df_btw,
                              self.ss_fA/self.df_fA,
                              self.ss_fB/self.df_fB,
                              self.ss_AB/self.df_AB,
                              self.ss_err/self.df_err]
        self.varianz_error = self.ss_err/self.df_err
        
    def f_fisher(self):
        self.f_calculated = [self.varianz_table[2]/self.varianz_table[5],
                             self.varianz_table[3]/self.varianz_table[5],
                             self.varianz_table[4]/self.varianz_table[5]]
        
        self.f_two_tails = [stats.f.ppf(1 - (self.alpha), self.df_fA, self.df_err),
                        stats.f.ppf(1 - (self.alpha), self.df_fB, self.df_err),
                        stats.f.ppf(1 - (self.alpha), self.df_AB, self.df_err)]
        
        self.f_table_range = [f"({custom_round(1/self.f_two_tails[0], 3)}, {custom_round(self.f_two_tails[0], 3)})",
                              f"({custom_round(1/self.f_two_tails[1], 3)}, {custom_round(self.f_two_tails[1], 3)})",
                              f"({custom_round(1/self.f_two_tails[2], 3)}, {custom_round(self.f_two_tails[2], 3)})"]

    # -----------------------------------
    def create_table(self):
        if (self.varianz_table[5] != 0):
            self.table_results = [[self.ss_tot, self.df_tot, self.varianz_table[0],0,0],
                              [self.ss_btw, self.df_btw, self.varianz_table[1],0,0],
                              [self.ss_fA, self.df_fA, self.varianz_table[2], self.f_calculated[0], self.f_table_range[0]],
                              [self.ss_fB, self.df_fB, self.varianz_table[3], self.f_calculated[1],self.f_table_range[1]],
                              [self.ss_AB, self.df_AB, self.varianz_table[4], self.f_calculated[2],self.f_table_range[2]],
                              [self.ss_err, self.df_err, self.varianz_table[5],0,0]]
            self.table_results_round = [[custom_round(float(self.table_results[i][j]), 3) if j!=4 else self.table_results[i][j]
                                         for j in range(5)] for i in range(6)]
        else:
            self.table_results = [[0 for _ in range(5)] for _ in range(6)]
    
    def plot_Fisher(self, ix: int, two_tail: bool = False): # 0=A, 1=B, 2=AB 
        self.delete_plot()
        
        # Calcular los valores críticos de F para ambas colas
        f_critica_izquierda = stats.f.ppf(self.alpha, self.DF_list[ix], self.df_err) if two_tail else None
        f_critica_derecha = stats.f.ppf(1 - (self.alpha), self.DF_list[ix], self.df_err) 

        max_x = round(f_critica_derecha*1.15)
        # Generar valores de la distribución F
        x = np.linspace(0, max_x, 1000)
        y = stats.f.pdf(x, self.DF_list[ix], self.df_err)

        # Crear la figura y el gráfico
        self.fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, label='Distribución F de Fisher', color='blue')

        if two_tail:
            # Rellenar la zona de rechazo por la cola izquierda
            # ax.fill_between(x, y, where=(x <= f_critica_izquierda), color='red', alpha=0.5, label='Zona de rechazo (cola izquierda)')
            plt.axvline(f_critica_izquierda, color='red', linestyle='--', label=f'F de rechazo izquierda = {custom_round(f_critica_izquierda)}')

        # Rellenar la zona de rechazo por la cola derecha
        # ax.fill_between(x, y, where=(x >= f_critica_derecha), color='red', alpha=0.5, label='Zona de rechazo (cola derecha)')
        plt.axvline(f_critica_derecha, color='red', linestyle='--', label=f'F de rechazo derecha = {custom_round(f_critica_derecha)}')

        ax.axvline(self.f_calculated[ix], color='green', linestyle='--', label=f'F calculada = {custom_round(self.f_calculated[ix])}')

        ax.set_title('Distribución F de Fisher y Zona de Rechazo')
        ax.set_xlabel('Valores de F')
        ax.set_ylabel('Densidad de probabilidad')
        ax.legend()
        return self.fig    

    def delete_plot(self):
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None

def custom_round(value, digits: int=3) -> str | float:
    if value == 0:
        return 0.0
    if abs(value) < 10**-2:
        return f"{value:.{digits}e}".replace("e", "x10^")
    else:
        return round(value, digits)