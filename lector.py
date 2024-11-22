import os

archivo_csv = "features_output.csv"

# Verificar si el archivo está vacío
if os.path.exists(archivo_csv) and os.stat(archivo_csv).st_size > 0:
    import pandas as pd
    df = pd.read_csv(archivo_csv)
    #print(df.head())
    #print(df.columns)
    #print(df.shape)
    print(df)
    df_10 = df
    df_10.to_html("tabla.html", index=False)
    print("La tabla se ha guardado como 'tabla.html'. Ábrela en tu navegador para visualizarla.")
else:
    print("El archivo está vacío o no existe.")
