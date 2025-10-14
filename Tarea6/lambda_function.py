#Jonathan Alexandro Pulido estrada
import boto3
import os
from import_csv import gen_df, convert_df_to_csv, send_csv
from mysql_utils import init_conn, create_df
                
#datos de conexion a mysql
host=os.environ['DB_HOST']
port=os.environ['DB_PORT']
dataBase=os.environ['DB_DATABASE']
user=os.environ['DB_USER']
password=os.environ['DB_PASS']
query ="select * from personas" 
#datos del bucket al que se enviará
send_to_bucket = os.environ['SEND_TO_BUCKET']    
target = "personas.csv"    

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        #conexcion a mysqll
        conn=init_conn(host, port, dataBase, user, password)

        #creamos el dataframe, recibe una conexion u un query
        df = create_df(conn , query)
        if df.empty:#por si el dataframe esta vacio
            return {
                'statusCode': 204,
                'body': 'No se encontraron datos.'
            }
        #vista previa del dataframe
        print(df.head().to_string())
        #convertimos el dataframe a csv con ayuda de la funcion en import_csv
        csv_buffer = convert_df_to_csv(df)
        #enviaos el csv al bucket con ayud de la funcion definida en import_csv
        send_csv(s3, csv_buffer, send_to_bucket, target)

        return {
            'statusCode': 200,
            'body': f"CSV cargado en el bucket!!",
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }