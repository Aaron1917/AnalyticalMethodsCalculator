import pandas as pd

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
    
def convert_RowxCol_Compact(df: pd.DataFrame, nameFA: str = 'Factor A', nameFB: str = 'FactorB', nameObs: str = 'Observaciones') -> pd.DataFrame:
    name_row = df.columns.to_list()[1:]
    print(name_row)
    for col in name_row:
        df[col] = df[col].str.split(r',\s*')

    df_expanded = df.explode(name_row, ignore_index=True)
    return convert_RowxCol2TwoCols(df_expanded, nameFA=nameFA, nameFB=nameFB, nameObs=nameObs,)

def convert_RowxCol2TwoCols(df: pd.DataFrame, nameFA: str = 'Factor A', nameFB: str = 'FactorB', nameObs: str = 'Observaciones') -> pd.DataFrame:
    name_col = df.columns.to_list()[0]

    df[name_col] = df[name_col].ffill()

    df_long = df.melt(id_vars=[name_col], var_name=nameFA, value_name=nameObs)

    df_long = df_long.rename(columns={name_col: nameFB})
    df_long = df_long[[nameFA, nameFB, nameObs]]
    return df_long

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
