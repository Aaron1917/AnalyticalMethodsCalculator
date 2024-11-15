import numpy as np
import pandas as pd
import stadistics.addons as ad


'''
https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc232.htm
Clase para calculos de ANOVA 2 factores cruzados con diseño equilibrado considerando un DataFrame
tabla de 2 columnas + columna de observaciones como el siguiente ejemplo:
Tabla 2 columnas + observaciones
        #   FactorA     FactorB     Observaciones
        0   A1          B1          data
        1   A1          B2          data
        2   A2          B1          data
        3   A2          B2          data
        ...        
'''

class Crossed2FactorAnova:

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
        self.grupos_B = self.data[self.headers[1]].unique()

        self.no_factorA = len(self.grupos_A)
        self.no_factorB = len(self.grupos_B)
        self.no_elements = self.data.shape[0] // (self.no_factorA * self.no_factorB)
        
        self.table_count_elements = self.data.groupby(self.headers[:2]).size().reset_index(name='Conteo')
        if not ad.same_items_list(self.table_count_elements['Conteo'].to_list()):
            raise ValueError(f'El número de {self.headers[2]} de cada combinación no está equilibrado')
        
        self.table_count_factorsB = self.data.groupby(self.headers[0])[self.headers[1]].nunique().reset_index(name='No.FactorB')
        if not ad.same_items_list(self.table_count_factorsB['No.FactorB'].to_list()):
            raise ValueError(f'El número de {self.headers[1]} de cada combinación no está equilibrado')
        
        if values is not None:
            if self.no_factorA != values[0]:
                raise ValueError(f'El número de {self.headers[0]} no coincide con los datos ingresados')
            if self.no_factorB != values[1]:
                raise ValueError(f'El número de {self.headers[1]} no coincide con los datos ingresados')
            if self.no_elements != values[2]:
                raise ValueError(f'El número de {self.headers[2]} no coincide con los datos ingresados')

    def calcular_media(self, data: pd.DataFrame):
        return np.mean(data)
    
    def calcular_media_grupos(self, data):
        resultados = []
        for a in self.grupos_A:
            for b in self.grupos_B:
                filtro = (data[self.headers[0]] == a) & (data[self.headers[1]] == b)
                # print(type(filtro)) # <class 'pandas.core.series.Series'>
                promedio = self.calcular_media(data[filtro][self.headers[2]])
                resultados.append({self.headers[0]: a, self.headers[1]: b, 'Promedio': promedio})
        return pd.DataFrame(resultados)
    
    def calcular_media_grupoA(self, data, grupos_A: list):
        resultados = []
        for a in grupos_A:
                filtro = (data[self.headers[0]] == a)
                promedio = self.calcular_media(data[filtro][self.headers[2]])
                resultados.append({self.headers[0]: a, 'Promedio': promedio})
        return pd.DataFrame(resultados)
    
    def calcular_media_grupoB(self, data, grupos_B: list):
        resultados = []
        for b in grupos_B:
                filtro = (data[self.headers[1]] == b)
                promedio = self.calcular_media(data[filtro][self.headers[2]])
                resultados.append({self.headers[1]: b, 'Promedio': promedio})
        return pd.DataFrame(resultados)


    def calcular_means(self):
        self.media_total = self.calcular_media(self.data[self.headers[2]])
        self.media_grupos = self.calcular_media_grupos(self.data)
        self.media_grupoA = self.calcular_media_grupoA(self.data, self.grupos_A)
        self.media_grupoB = self.calcular_media_grupoB(self.data, self.grupos_B)

        '''print(f"la media total es: {self.media_total}")
        print(f"El df con promedios por grupos es: \n{self.media_grupos}")
        print(f"El df con promedios por grupo A es: \n{self.media_grupoA}")
        print(f"El df con promedios por grupo B es: \n{self.media_grupoB}")'''

    def calcular_sst(self, data: pd.DataFrame):
        return np.sum((data - self.media_total) ** 2)
    
    def calcular_ssbtw(self, data: pd.DataFrame):
        sumatoria = ((data['Promedio'] - self.media_total) ** 2).sum()
        return self.no_elements * sumatoria


    def calcular_ssa(self, data: pd.DataFrame): 
        sumatoria = ((data['Promedio'] - self.media_total) ** 2).sum()
        return self.no_factorB * self.no_elements * sumatoria

    def calcular_ssb(self, data: pd.DataFrame):
        sumatoria = ((data['Promedio'] - self.media_total) ** 2).sum()
        return self.no_factorA * self.no_elements * sumatoria
    
    def calcular_ssab(self):
        return self.ssbtw - self.ssa -self.ssb
    
    def calcular_sse(self, data: pd.DataFrame):
        sumatoria = []

        for a in self.grupos_A:
            for b in self.grupos_B:
                filtro_data = (data[self.headers[0]] == a) & (data[self.headers[1]] == b)
                filtro_mean = (self.media_grupos[self.headers[0]] == a) & (self.media_grupos[self.headers[1]] == b)

                datos_filtrados = data.loc[filtro_data, self.headers[2]]
                media = self.media_grupos.loc[filtro_mean, 'Promedio'].iloc[0]

                sumatoria.append(((datos_filtrados - media) ** 2).sum())
        return sum(sumatoria)

    
    def calcular_ss(self):
        self.sst = self.calcular_sst(self.data[self.headers[2]])
        self.ssbtw = self.calcular_ssbtw(self.media_grupos)
        self.ssa = self.calcular_ssa(self.media_grupoA)
        self.ssb = self.calcular_ssb(self.media_grupoB)
        self.ssab = self.calcular_ssab()
        self.sse = self.calcular_sse(self.data)
    
    def calcular_dft(self):
        return (self.no_elements * self.no_factorA * self. no_factorB) - 1
    
    def calcular_dfbtw(self):
        return (self.no_factorA * self. no_factorB) - 1
    
    def calcular_dfa(self):
        return self.no_factorA - 1
    
    def calcular_dfb(self):
        return self.no_factorB -1
    
    def calcular_dfab(self):
        return (self.no_factorA - 1) * (self.no_factorB - 1)
    
    def calcular_dfe(self):
        return (self.no_elements - 1) * self.no_factorA * self. no_factorB

    def calcular_df(self):
        self.dft = self.calcular_dft()
        self.dfbtw = self.calcular_dfbtw()
        self.dfa = self.calcular_dfa()
        self.dfb = self.calcular_dfb()
        self.dfab = self.calcular_dfab()
        self.dfe = self.calcular_dfe()

    def calcular_mst(self):
        return self.sst / self.dft

    def calcular_msbtw(self):
        return self.ssbtw / self.dfbtw
    
    def calcular_msa(self):
        return self.ssa / self.dfa
    
    def calcular_msb(self):
        return self.ssb / self.dfb
    
    def calcular_msab(self):
        return self.ssab / self.dfab
    
    def calcular_mse(self):
        return self.sse / self.dfe

    def calcular_ms(self):
        self.mst = self.calcular_mst()
        self.msbtw = self.calcular_msbtw()
        self.msa = self.calcular_msa()
        self.msb = self.calcular_msb()
        self.msab = self.calcular_msab()
        self.mse = self.calcular_mse()

    def calcular_fa(self):
        return self.msa / self.mse
    
    def calcular_fb(self):
        return self.msb / self.mse
    
    def calcular_fab(self):
        return self.msab / self.mse
    
    def calcular_f(self):
        self.fa = self.calcular_fa()
        self.fb = self.calcular_fb()
        self.fab = self.calcular_fab()
        

    def calculate_anova_table(self)-> pd.DataFrame:
        self.calcular_means()
        self.calcular_ss()
        self.calcular_df()
        self.calcular_ms()
        self.calcular_f()

        results = {
            'Factor de Variación': ['Total', 'Between', self.headers[0], self.headers[1], 'Interacción', 'Error'],
            'Suma de cuadrados ': [self.sst, self.ssbtw, self.ssa, self.ssb, self.ssab, self.sse],
            'Grados de libertad': [self.dft, self.dfbtw, self.dfa, self.dfb, self.dfab, self.dfe],
            'Media de cuadrados': [self.mst, self.msbtw, self.msa, self.msb, self.msab, self.mse],
            'F. Calculada': ['', '', self.fa, self.fb, self.fab, '']
        }
        return pd.DataFrame(results)

    
        
# Ejemplo de uso
if __name__ == "__main__":
    # test
    print("Test")
    data = {
        'Factor A': ['A1', 'A1', 'A2', 'A2'],
        'Factor B': ['B1', 'B2', 'B1', 'B2'],
        'Observaciones': [
            [85.0, 90, 88, 92],  # A1B1
            [80, 78.0, 83, 79],  # A1B2
            [91, 93.0, 89, 94],  # A2B1
            [87, 85, 90, 88.0]   # A2B2
        ]
    }
    data = ad.convert_dicct2DataFrame(data)
    print()

    anova_croseed = Crossed2FactorAnova(data) 
    anova_cros = anova_croseed.calculate_anova_table()
    print(pd.DataFrame(anova_cros))