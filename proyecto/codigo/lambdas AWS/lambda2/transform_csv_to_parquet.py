import boto3
import pandas as pd
import io
import os

# get last csv name
def get_csv_name(s3, bucket, prefix):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    contents = response.get('Contents', [])

 
    files = [obj['Key'] for obj in contents if not obj['Key'].endswith('/')]

    if not files:
        return None

    
    file_key = files[0].strip()
    print(f"Archivo encontrado: {file_key}")
    return file_key


# csv to dataframe
def csv_to_df(s3, bucket, file_key):
    response = s3.get_object(Bucket=bucket, Key=file_key)
    body = response['Body'].read()
    df = pd.read_csv(io.BytesIO(body))
    return df


# delete columns
def delete_columns_df(df):
    # Verificar que haya al menos las columnas esperadas
    columnas_a_eliminar = [0, 2, 3, 7, 9, 10]
    columnas_validas = [i for i in columnas_a_eliminar if i < len(df.columns)]
    df_result = df.drop(df.columns[columnas_validas], axis=1)
    return df_result


# rename columns and transform to datetime
def transform_df(df):
    df['fecha'] = pd.to_datetime(df['fecha'])

    df = df.rename(columns={
        "fecha": "Fecha de producción",
        "cantidad": "Cantidad producida",
        "precio": "Costo por litro producido",
        "costo_produccion": "Costo de la producción",
        "descripcion": "Tipo de pintura producida",
        "nombre": "Operador"
    })

    
    df["Tipo de pintura producida"] = df["Tipo de pintura producida"].str.capitalize()

    # reorder
    columnas_orden = [
        "Fecha de producción",
        "Tipo de pintura producida",
        "Cantidad producida",
        "Costo por litro producido",
        "Costo de la producción",
        "Operador"
    ]
    df = df[columnas_orden]
    return df


# dataframe to csv
def convert_df_to_csv(df):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer


# dataframe to parquet
def convert_df_to_parquet(df):
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    return parquet_buffer


# upload file to bucket
def send_file_to_s3(s3, file_buffer, bucket, key, is_parquet=False):
    content_type = "application/octet-stream" if is_parquet else "text/csv"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=file_buffer.getvalue(),
        ContentType=content_type
    )
    print(f"Archivo enviado a S3: s3://{bucket}/{key}")


# delete last csv read
def delete_csv(s3, bucket, file_path):
    s3.delete_object(Bucket=bucket, Key=file_path)
    print(f"Archivo eliminado: s3://{bucket}/{file_path}")
