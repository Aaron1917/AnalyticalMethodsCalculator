import numpy as np
import pandas as pd
import stadistics.addons as ad


'''
#https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc233.htm
Clase para calculos de ANOVA 2 factores anidados con diseño equilibrado considerando un DataFrame
tabla de 2 columnas + columna de observaciones como el siguiente ejemplo:
Tabla 2 columnas + observaciones
        #   FactorA     FactorB     Observaciones
        0   A1          B1          data
        1   A1          B2          data
        2   A2          B1          data
        3   A2          B2          data
        ...        
'''
class Nested2FactorAnava():

    def __init__(self, data: pd.DataFrame = None,
                 values: list | tuple = None,
                 alpha: float=0.05):
        self.alpha = alpha
        self.headers = data.columns.to_list()
        self.data = ad.apply_funtion_df(data, ad.replace_nan_string)
        self.data[self.headers[2]] = pd.to_numeric(self.data[self.headers[2]], errors='coerce')
        if self.data.isna().any().any():
            raise ValueError('Alguno de los datos no es válido, favor de revisarlos.')
        
        self.grupos_A = self.data[self.headers[0]].unique()
        self.no_factorA = len(self.grupos_A)

        self.grupos_B = [
            self.data[self.data[self.headers[0]] == a][self.headers[1]].unique().tolist()
            for a in self.grupos_A
        ]
        
        self.no_factorB = [len(b) for b in self.grupos_B]

        elements = [[
                self.data[(self.data[self.headers[0]] == a) & (self.data[self.headers[1]] == b)][self.headers[2]].to_list()
                for b in self.grupos_B[iter]]
                for iter, a in enumerate(self.grupos_A)
                ]

        self.no_elements = [[len(e) for e in sublist] for sublist in elements]

        self.table_count_elements = self.data.groupby(self.headers[:2]).size().reset_index(name='Conteo')
        if not ad.same_items_list(self.table_count_elements['Conteo'].to_list()):
            raise ValueError(f'El número de {self.headers[2]} de cada combinación no está equilibrado')
        
        self.table_count_factorsB = self.data.groupby(self.headers[0])[self.headers[1]].nunique().reset_index(name='No.FactorB')
        if not ad.same_items_list(self.table_count_factorsB['No.FactorB'].to_list()):
            raise ValueError(f'El número de {self.headers[1]} de cada combinación no está equilibrado')

        if values is not None:
            if self.no_factorA != values[0]:
                raise ValueError(f'El número de {self.headers[0]} no coincide con los datos ingresados')
            if self.no_factorB[0] != values[1]:
                raise ValueError(f'El número de {self.headers[1]} no coincide con los datos ingresados')
            if self.no_elements[0][0] != values[2]:
                raise ValueError(f'El número de {self.headers[2]} no coincide con los datos ingresados')

    def calcular_media(self, data: pd.DataFrame):
        return np.mean(data)

    def calcular_media_grupoA(self, data: pd.DataFrame, grupos_A: list):
        results = []
        for a in grupos_A:
            filtro = (data[self.headers[0]] == a)
            promedio = self.calcular_media(data[filtro][self.headers[2]])
            results.append({self.headers[0] : a,'Promedio': promedio})
        return pd.DataFrame(results)
    
    def calcular_media_grupoB(self, data: pd.DataFrame, grupos_A: list, grupos_B: list):
        results = []
        for i, a in enumerate(grupos_A):
            for b in grupos_B[i]:
                filtro = (self.data[self.headers[0]] == a) & (self.data[self.headers[1]] == b)
                promedio = self.calcular_media(data[filtro][self.headers[2]])
                results.append({self.headers[0] : a, self.headers[1] : b,'Promedio' : promedio})
        return pd.DataFrame(results)

    def calcular_means(self):
        self.media_total = self.calcular_media(self.data[self.headers[2]])
        self.media_grupoA = self.calcular_media_grupoA(self.data, self.grupos_A)
        self.media_grupoB = self.calcular_media_grupoB(self.data, self.grupos_A, self.grupos_B)

        # print(f"La media total es: \n{self.media_total}")
        # print(f"La media de grupos A es: \n{self.media_grupoA}")
        # print(f"La media de grupos B es: \n{self.media_grupoB}")

    def calcular_sst(self, data: pd.DataFrame):
        return np.sum((data - self.media_total) ** 2)

    def calcular_ssa(self, data: pd.DataFrame):
        result = 0
        for i, a in enumerate(self.grupos_A):
            sumatoria = (data[data[self.headers[0]] == a]['Promedio'].iloc[0] - self.media_total) ** 2
            result += sum(self.no_elements[i]) * sumatoria
        return result
    
    def calcular_ssb(self, data_a: pd.DataFrame, data_b: pd.DataFrame):
        result = 0
        for i, a in enumerate(self.grupos_A):
            for j, b in enumerate(self.grupos_B[i]):
                filtro = (data_b[self.headers[0]] == a) & (data_b[self.headers[1]] == b)
                sumatoria = (data_b[filtro]['Promedio'].iloc[0] - data_a[data_a[self.headers[0]] == a]['Promedio'].iloc[0]) ** 2
                result += self.no_elements[i][j] * sumatoria
        return result
    
    def calcular_sse(self, data_p: pd.DataFrame):#residual
        result = 0
        for i, a in enumerate(self.grupos_A):
            for b in self.grupos_B[i]:
                filtro_data = (self.data[self.headers[0]] == a) & (self.data[self.headers[1]] == b)
                filtro_mean = (data_p[self.headers[0]] == a) & (data_p[self.headers[1]] == b)
                sumatoria = ((self.data[filtro_data][self.headers[2]] - data_p[filtro_mean]['Promedio'].iloc[0]) ** 2).sum()
                result += sumatoria
        return result

    def calcular_ss(self): 
        self.sst = self.calcular_sst(self.data[self.headers[2]])
        self.ssa = self.calcular_ssa(self.media_grupoA)
        self.ssb = self.calcular_ssb(self.media_grupoA, self.media_grupoB)
        self.sse = self.calcular_sse(self.media_grupoB)

    def calcular_dft(self):
        return (self.no_factorA * self.no_factorB[0] * self.no_elements[0][0]) - 1

    def calcular_dfa(self):
        return self.no_factorA -1 

    def calcular_dfb(self):
        return self.no_factorA * (self.no_factorB[0] - 1)

    def calcular_dfr(self):
        return self.no_factorA * self.no_factorB[0] * (self.no_elements[0][0] - 1)

    def calcular_df(self):
        self.dft = self.calcular_dft()
        self.dfa = self.calcular_dfa()
        self.dfb = self.calcular_dfb()
        self.dfe = self.calcular_dfr()

    def calcular_msa(self):
        return self.ssa / self.dfa
    
    def calcular_msb(self):
        return self.ssb / self.dfb
    
    def calcular_mse(self): 
        return self.sse / self.dfe

    def calcular_ms(self):
        self.msa = self.calcular_msa()
        self.msb = self.calcular_msb()
        self.mse = self.calcular_mse()

    def calcular_fa(self):
        return self.msa / self.msb
    
    def calcular_fb(self):
        return self.msb / self.mse

    def calcular_f(self):
        self.fa = self.calcular_fa()
        self.fb = self.calcular_fb()

    def calculate_anova_table(self):
        self.calcular_means()
        self.calcular_ss()
        self.calcular_df()
        self.calcular_ms()
        self.calcular_f()
        results = {
            'Factor de Variación': ['Total', self.headers[0], f'{self.headers[1]} en {self.headers[0]}', 'Error'],
            'Suma de cuadrados ': [self.sst, self.ssa, self.ssb, self.sse],
            'Grados de libertad': [self.dft, self.dfa, self.dfb, self.dfe],
            'Media de cuadrados': ['', self.msa, self.msb, self.mse],
            'F. calculada': ['', self.fa, self.fb, '']
        }
        return pd.DataFrame(results)

if __name__ == "__main__":
    print("test")
    '''
    Escuela 1: 2 clases (Clase A y Clase B)
    Escuela 2: 2 clases (Clase A y Clase B)
    Escuela 3: 3 clases (Clase A y Clase B)
    2 estudiantes por clase
    '''
    example = {
        'FA' : ['E1', 'E1', 'E1', 'E1', 'E2', 'E2', 'E2', 'E2', 'E3', 'E3', 'E3', 'E3'],
        'FB' : ['CA', 'CA', 'CB', 'CB', 'CA', 'CA', 'CB', 'CB', 'CA', 'CA', 'CB', 'CB'],
        'Cal': [85, 63, 86, 87, 84, 73, 96, 88, 75, 93, 86, 77]
    }

    datos = pd.DataFrame(example)
    anova_nested = Nested2FactorAnava(data=datos)
    table = anova_nested.calculate_anova_table()
    print(table)