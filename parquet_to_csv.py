import boto3
import pandas as pd
import io
from last_folder import get_last_folder_in_production
from last_file import get_last_file_in_folder

BUCKET_NAME = "xideralaws-curso-jonathan"
carpeta = get_last_folder_in_production(BUCKET_NAME)
path = f"produccion/{carpeta}"
file = get_last_file_in_folder(BUCKET_NAME , path)
parquet_key = f"{path}{file}"
print(f"Ruta completa: {parquet_key}")
print(carpeta)
print(file)

# Leer parquet desde S3
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=parquet_key)
parquet_buffer = io.BytesIO(obj['Body'].read())
df = pd.read_parquet(parquet_buffer)

output_csv = "datos_ultima_produccion.csv"
df.to_csv(output_csv, index=False)
print(f"CSV guardado como: {output_csv}")
print(f"Filas: {len(df)}, Columnas: {len(df.columns)}")