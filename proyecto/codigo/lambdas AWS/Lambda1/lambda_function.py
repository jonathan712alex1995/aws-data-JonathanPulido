# Jonathan Alexandro Pulido Estrada
import boto3
import os
from datetime import timedelta
from import_csv import *
from mysql_utils import *

# Datos de conexión a MySQL
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
dataBase = os.environ['DB_DATABASE']
user = os.environ['DB_USER']
password = os.environ['DB_PASS']
send_to_bucket = os.environ['SEND_TO_BUCKET']
target = "crudos/"

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    try:
        fecha = get_last_date(s3, send_to_bucket) + timedelta(days=1)
        #Conexión a MySQL
        conn = init_conn(host, port, dataBase, user, password)

        
        query = f"""
            SELECT * 
            FROM produccion pp
            JOIN productos p ON pp.id_producto = p.id_producto
            JOIN operadores op ON pp.id_operador = op.id_operador
            WHERE pp.fecha = '{fecha}'
        """
        #create dataframe
        df = create_df(conn, query)

        if df.empty:
            save_last_date(fecha, s3, send_to_bucket)
            return {
                'statusCode': 204,
                'body': f"No se encontraron datos para {fecha}. Fecha actualizada."
            }
        #set foldername and filename
        folder_name = fecha.strftime("%Y-%m")
        file_name = f"produccion_{fecha}.csv"
        key = f"{target}{file_name}"
        #dataframe to csv
        parquet_buffer = convert_df_to_csv(df)
        #send to bucket
        send_csv_or_parquet(s3, parquet_buffer, send_to_bucket, key)
        #update last date
        save_last_date(fecha, s3, send_to_bucket)

        return {
            'statusCode': 200,
            'body': f" Archivo guardado correctamente para la fecha {fecha}."
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
