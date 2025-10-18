import mysql.connector
import pandas as pd
import boto3
from datetime import date, timedelta, timezone, datetime

#Jonathan Alexandro Pulido Estrada
#funcion para iniciar una conexion a la base de datos
def init_conn(host, port, dataBase, user, password):
    try:
        cnx=mysql.connector.connect(
        host=host,
        port=int(port),
        database=dataBase,
        user=user,
        password=password
        )
        print("conexion establecida!!!")
        return cnx
    except Exception as e:
        print("error en la conexion, verifica las variables de entorno!!")
        return None

#funcion para creaer el dataframe a partir de la consulta
def create_df(conn , query):
    cur = conn.cursor()
    query = cur.execute(query)
    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    df = pd.DataFrame(filas,columns=columnas)
    cur.close()
    return df

"""
#delete columns
def delete_columns_df(df):
    df_result = df.drop(columns=[df.columns[0], df.columns[2], df.columns[3], df.columns[7], df.columns[9], df.columns[10]])
    return df_result
"""
#get last date 
def get_last_date(s3, bucket):
    obj = s3.get_object(Bucket=bucket, Key="checkpoints/ultima_fecha.txt")
    fecha_str = obj['Body'].read().decode('utf-8').strip()
    print(fecha_str)
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()

#save last date
def save_last_date(fecha , s3 , bucket):
    """Guarda la nueva fecha en S3 para la próxima ejecución."""
    s3.put_object(Bucket=bucket, Key="checkpoints/ultima_fecha.txt", Body=str(fecha))