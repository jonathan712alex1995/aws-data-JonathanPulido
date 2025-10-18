import json
import boto3
import os
from transform_csv_to_parquet import *

bucket = "xideralaws-curso-jonathan"
prefix = "crudos/"
target = "produccion/"
s3 = boto3.client('s3')

def lambda_handler(event, context):
    #get last csv
    file_path = get_csv_name(s3, bucket, prefix)

    if not file_path:
        return {
            'statusCode': 204,
            'body': "No se encontró ningún archivo en la carpeta 'crudos/'."
        }

    # read and transform
    df = csv_to_df(s3, bucket, file_path)
    df = delete_columns_df(df)
    df = transform_df(df)

    # to parquet
    file_buffer = convert_df_to_parquet(df)

    # set file name 
    file_name = os.path.basename(file_path).replace(".csv", "")

    if "_" in file_name:
        folder_name = file_name.split("_")[1][:7]
    else:
        folder_name = "otros"

    key = f"{target}{folder_name}/{file_name}.parquet"

    # send parquet to bucket
    send_file_to_s3(s3, file_buffer, bucket, key, is_parquet=True)

    # delete last csv read
    delete_csv(s3, bucket, file_path)

    return {
        'statusCode': 200,
        'body': f"Archivo procesado y movido a {key}"
    }
