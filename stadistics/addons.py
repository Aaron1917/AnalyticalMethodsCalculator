import pandas as pd
import numpy as np

def convert_dicct2DataFrame(data: dict,
                            name_col1: str ="Factor A",
                            name_col2: str ="Factor B",
                            name_col3: str ="Observaciones"
                            ) -> pd.DataFrame:
    if len(data) != 3:
        raise RuntimeError("Argument 'data' no valid")
    observaciones = []
    df = pd.DataFrame(data)
    headers = df.columns.to_list()
    for index, row in df.iterrows():
        for obs in row[headers[2]]:
            observaciones.append({name_col1: row[headers[0]], name_col2: row[headers[1]], name_col3: obs})

    return pd.DataFrame(observaciones)
    
def convert_RxCc2RxC(df: pd.DataFrame) -> pd.DataFrame:

    name_row = df.columns.to_list()[1:]
    for col in name_row:
        df[col] = df[col].str.split(r',\s*')
    df_expanded = df.explode(name_row, ignore_index=True)
    # print(df_expanded)
    for col in name_row:
        #print(df_expanded[col])
        # df_expanded[col] = df_expanded[col].replace('', np.nan)
        #df_expanded[col] = df_expanded[col].apply(lambda x: np.nan if x == '' else x)
        #df_expanded[col] = df_expanded[col].apply(lambda x: float(x) if pd.notna(x) else np.nan)
        df_expanded[col] = df_expanded[col].apply(lambda x: np.nan if x == str(np.nan) else float(x))
    #print(f"\n la RxC es:\n{df_expanded}")
    return df_expanded

def convert_RxC2ThreeCol(df: pd.DataFrame, nameFA: str = 'FactorA', nameFB: str = 'FactorB', nameObs: str = 'Observaciones') -> pd.DataFrame:
    name_col = df.columns.to_list()[0]

    df[name_col] = df[name_col].ffill()

    df_long = df.melt(id_vars=[name_col], var_name=nameFA, value_name=nameObs)

    df_long = df_long.rename(columns={name_col: nameFB})
    df_long = df_long[[nameFA, nameFB, nameObs]]
    return df_long

def convert_RxC2RxCc(df: pd.DataFrame):
    df_result = df.groupby('Factores').agg(lambda x: ', '.join(map(str, x))).reset_index()
    return df_result

def convert_ThreeCol2RxCc(df: pd.DataFrame):
    headers = df.columns.to_list()
    #df = df.fillna('').astype(str)
    df_pivot = df.groupby([headers[1], headers[0]])[headers[2]].apply(lambda x: ', '.join(map(str, x))).unstack()

    df_pivot.index.name = 'Factores'
    df_pivot.columns.name = None
    return df_pivot.reset_index()

def apply_funtion_df(df: pd.DataFrame, fun) -> pd.DataFrame:
    headers = df.columns.to_list()
    for h in headers:
        df[h] = df[h].apply(lambda x: fun(x))

    return df
def same_items_list(list: list) -> bool:
    return True if len(set(list)) == 1 else False

def custom_round(value: str | float, digits: int=3) -> str | float:
    if type(value) == type(str()):
        return value
    if value == 0:
        return 0.0
    if abs(value) < 10**-2:
        return f"{value:.{digits}e}".replace("e", "x10^")
    else:
        return round(value, digits)


if __name__ == "__main__":
    data = {
        'Factores': ['FactorB 1', 'FactorB 1', 'FactorB 2', 'FactorB 2', 'FactorB 3', 'FactorB 3', 'FactorB 4', 'FactorB 4'],
        'FactorA 1': [1.1, 1.2, 1.3, 1.4, 1.55, 1.6, 1.7, 1.8],
        'FactorA 2': [6.1, 6.23, 6.12, 6.13, 6.14, 6.15, 6.16, 6.18]
    }
    df = pd.DataFrame(data)
    print(f"Data frame inicial\n{df}")

    df1 = convert_RxC2RxCc(df=df)
    print(f"Data frame RxCc\n{df1}")

    df2 = convert_RxCc2RxC(df=df1)
    print(f"Data frame RxC\n{df2}")

    df3 = convert_RxC2ThreeCol(df=df2)
    print(f"Data frame ThreeCol\n{df3}")

    df4 = convert_ThreeCol2RxCc(df=df3)
    print(f"Data frame RxCc\n{df4}")