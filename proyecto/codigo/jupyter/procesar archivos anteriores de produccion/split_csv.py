import pandas as pd
import os


df = pd.read_csv("produccion_2025_06.csv")


df['fecha'] = pd.to_datetime(df['fecha'])


output_folder = 'archivos_por_dia'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


fechas_unicas = df['fecha'].dt.date.unique()

print(f"Se encontraron {len(fechas_unicas)} fechas únicas\n")


for fecha in fechas_unicas:
    # Filtrar datos de esa fecha
    df_fecha = df[df['fecha'].dt.date == fecha]
    
  
    df_fecha = df_fecha.rename(columns={
        "fecha": "Fecha de producción",
        "cantidad": "Cantidad producida",
        "precio": "Costo por litro producido",
        "total": "Costo de la producción",
        "producto": "Tipo de pintura producida",
        "operador": "Operador"
    })
    
   
    df_fecha["Tipo de pintura producida"] = df_fecha["Tipo de pintura producida"].str.capitalize()
    
    
    columnas_orden = [
        "Fecha de producción",
        "Tipo de pintura producida",
        "Cantidad producida",
        "Costo por litro producido",
        "Costo de la producción",
        "Operador"
    ]
    df_fecha = df_fecha[columnas_orden]
    
  
    fecha_str = pd.to_datetime(fecha).strftime('%Y-%m-%d')
    output_file = os.path.join(output_folder, f'produccion_{fecha_str}.parquet')
    
   
    df_fecha.to_parquet(output_file, index=False, engine='pyarrow')
    
    