
import pandas as pd
import streamlit as st
import plotly.express as px 
import matplotlib.pyplot as plt
import boto3
import json
import subprocess

st.set_page_config(page_title="Servers dashboard", layout="wide")


#funciones----------------------------------------------------------------------
def actualizar_datos():
        subprocess.run([
            "jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--inplace", "/home/ubuntu/buckets.ipynb"
        ], check=True)
        
def servidores_ok(df):
    filtrados=df[df["status"]=="OK"]
    result=filtrados.groupby("server_id")["status"].value_counts()
    return result

def servidores_warn(df):
    filtrados=df[df["status"]=="WARN"]
    result=filtrados.groupby("server_id")["status"].value_counts()
    return result

def servidores_error(df):
    filtrados=df[df["status"]=="ERROR"]
    result=filtrados.groupby("server_id")["status"].value_counts()
    return result


#creacion del dataframe-------------------------------------------------------------
df=pd.read_csv("datos_bucket.csv" , encoding='utf-8')
df_ok=servidores_ok(df)
df_warn=servidores_warn(df)
df_error=servidores_error(df)


st.title("Servers dashboard")

#boyton para actualizar los datos---------------------------------------------------
if st.button("Actualizar datos"):
    with st.spinner("Actualizando datos..."):
        actualizar_datos()
        df = pd.read_csv("/home/ubuntu/datos_bucket.csv" , encoding='utf-8')
        df_ok=servidores_ok(df)
        df_warn=servidores_warn(df)
        df_error=servidores_error(df)


#filtros del sidebar----------------------------------------------------------------------
st.sidebar.header("Filtros")
#status de los servidores
status_filter = st.sidebar.multiselect("Status", options=df['status'].unique(), 
default=df['status'].unique())
#servidores
servers_filter = st.sidebar.multiselect("server_id", options=df['server_id'].unique(), 
default=df['server_id'].sort_values().unique())
#Regiones
regions_filter=st.sidebar.multiselect("Region", options=df['region'].unique(),
default=df['region'].sort_values().unique())

filtered_df = df[(df['status'].isin(status_filter)) & (df['server_id'].isin(servers_filter)) & (df["region"].isin(regions_filter))]

#KPI-------------------------------------------------------------------------------
total_servers= (df["server_id"].nunique())
total_region = (df["region"].nunique())
total_data = len(df)

#Metricas--------------------------------------------------------------------------
col1, col2, col3= st.columns(3)
col1.metric("Total de datos", total_data)
col2.metric("Servidores", total_servers)
col3.metric("Regiones", total_region)


#Graficos----------------------------------------------------------------------------
col1, col2 , col3 = st.columns(3)
 
with col1:
    servers_count =df["server_id"].value_counts().sort_values(ascending=False)
    plt.figure(figsize=(5,3))
    fig1 = px.bar(
        servers_count,
        labels={"x": "Servidor", "y": "Cantidad"},
        title="Cantidad por servidor"
    )
    st.plotly_chart(fig1,use_container_width=True)
    
with col2:
    fig2 = px.pie(filtered_df, names="server_id", title="Servidores")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.pie(filtered_df, names="region", title="Regiones")
    st.plotly_chart(fig3, use_container_width=True)


#tabla con informacion de los servidores---------------------------------------------------
st.markdown("Detalle por estado de servidores")

table1, table2, table3 = st.columns(3)

with table1:
    st.subheader("OK")
    st.dataframe(df_ok)

with table2:
    st.subheader("WARN")
    st.dataframe(df_warn)

with table3:
    st.subheader("ERROR")
    st.dataframe(df_error)
#-------------------------------------------------------------------------------------------












