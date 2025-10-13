import json
import boto3
import pandas as pd
import io
from import_csv import gen_df, convert_df_to_csv, send_csv

#bucket origen
bucket_name = "xideralaws-curso-benjamin2" 
prefix = "raw/"                            
#bucket destino
send_to = "xideralaws-curso-jonathan"    
target = "datos_bucket_from_lambda.csv"    

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        df = gen_df(s3, bucket_name, prefix)

        if df.empty:#por si el dataframe esta vacio
            return {
                'statusCode': 204,
                'body': 'No se encontraron archivos JSON.'
            }

        csv_buffer = convert_df_to_csv(df)
        send_csv(s3, csv_buffer, send_to, target)

        return {
            'statusCode': 200,
            'body': f"CSV cargado en s3://{send_to}/{target}",
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
