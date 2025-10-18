import subprocess
import pandas as pd
import streamlit as st
from last_folder import get_last_folder_in_production
from last_file import get_last_file_in_folder
import boto3
import io

@st.cache_data(ttl=60)
def get_parquet(refresh_count=0):
    BUCKET_NAME = "xideralaws-curso-jonathan"
    carpeta = get_last_folder_in_production(BUCKET_NAME)
    path = f"produccion/{carpeta}"
    file = get_last_file_in_folder(BUCKET_NAME , path)
    parquet_key = f"{path}{file}"
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=parquet_key)
    parquet_buffer = io.BytesIO(obj['Body'].read())
    df = pd.read_parquet(parquet_buffer)
    return df


def production_per_operator(df):
    result = df.groupby("Operador", as_index=False)["Cantidad producida"].sum().sort_values(by="Cantidad producida" , ascending=True)
    return result
    
def total_per_paint(df):
    result = df.groupby("Tipo de pintura producida", as_index=False)["Cantidad producida"].sum().sort_values(by="Cantidad producida" , ascending=False)
    return result

def total_cost_per_paint(df):
    result = df.groupby("Tipo de pintura producida", as_index=False)["Costo de la producción"].sum()
    return result