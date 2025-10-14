import json
import boto3
import pandas as pd
import io

#para generar el dataframe del json
def gen_df(s3, bucket_name, prefix):
    response = s3.list_objects_v2(Bucket=bucket_name , Prefix = prefix)
    data_frames = []
    for obj in response["Contents"]:
        key = obj["Key"]
        if key.endswith(".json"):
            file_obj = s3.get_object(Bucket = bucket_name , Key= key)
            content = file_obj["Body"].read().decode("utf-8")
            json_data = json.loads(content)
            df_temp = pd.json_normalize(json_data)
            data_frames.append(df_temp)
    df=pd.concat(data_frames , ignore_index=True)
    return df

#convertir a csv
def convert_df_to_csv(df):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer

#enviar a bucket destino 
def send_csv(s3, csv_buffer, bucket, key):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer.getvalue()
    )


#codigo para el archivo test
"""
#Jonathan Alexandro Pulido estrada
import boto3
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
"""


