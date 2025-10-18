import subprocess
import pandas as pd
import streamlit as st

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv("/home/ubuntu/proyecto/datos_ultima_produccion.csv" , encoding='utf-8')

def update_dashboard():
    subprocess.run([
        "python", "/home/ubuntu/proyecto/parquet_to_csv.py"
    ], check=True)

def production_per_operator(df):
    result = df.groupby("Operador", as_index=False)["Cantidad producida"].sum().sort_values(by="Cantidad producida" , ascending=True)
    return result
    
def total_per_paint(df):
    result = df.groupby("Tipo de pintura producida", as_index=False)["Cantidad producida"].sum().sort_values(by="Cantidad producida" , ascending=False)
    return result

def total_cost_per_paint(df):
    result = df.groupby("Tipo de pintura producida", as_index=False)["Costo de la producción"].sum()
    return result