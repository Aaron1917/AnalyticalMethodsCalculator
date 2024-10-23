import numpy as np
import pandas as pd


'''
#https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc233.htm
Clase para calculos de ANOVA 2 factores anidados considerando un DataFrame
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

    def __init__(self, data: pd.DataFrame, alpha: float = 0.05):
        self.headers = data.columns.to_list()
        
        self.data = data
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
        self.alpha = alpha


        

if __name__ == "__main__":
    print("test")
    '''
    Escuela 1: 2 clases (Clase A y Clase B)
    Escuela 2: 2 clases (Clase C y Clase D)
    Escuela 3: 3 clases (Clase A, Clase B y Clase D)
    2 estudiantes por clase
    
    '''
    example = {
        'FA' : ['E1', 'E1', 'E1', 'E1', 'E2', 'E2', 'E2', 'E2', 'E3', 'E3', 'E3', 'E3', 'E3', 'E3'],
        'FB' : ['CA', 'CA', 'CB', 'CB', 'CC', 'CC', 'CD', 'CD', 'CA', 'CA', 'CB', 'CB', 'CC', 'CC'],
        'Cal': [85, 63, 86, 87, 84, 73, 96, 88, 75, 93, 86, 77, 95, 83]
    }
    datos = pd.DataFrame(example)
    anova_nested = Nested2FactorAnava(data=datos)
    #print(anov)