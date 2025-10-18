import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.express as px 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import pandas as pd
from functions_app_dashboard_produccion import *

st.set_page_config(page_title="Producción dashboard", layout="wide")
count = st_autorefresh(interval=60000, limit=None, key="datarefresh")
update_dashboard()
st.cache_data.clear()
df=load_data()

st.title("Dashboard de última producción")

#KPIs
date=df["Fecha de producción"][1]
operators= (df["Operador"].nunique())
paints = (df["Tipo de pintura producida"].nunique())
total_quantity = df["Cantidad producida"].sum()
cost=df["Costo de la producción"].sum()


#Metricas--------------------------------------------------------------------------
col1, col2, col3, col4, col5= st.columns(5)
col1.metric("Fecha", date)
col2.metric("Operadores", operators)
col3.metric("Tipos de pintura", paints)
col4.metric("Total de litros producidos", total_quantity)
col5.metric("Costo de la producción", cost)

# Después de tus métricas
st.divider()

col1, col2, col3 = st.columns(3)

# Gráfico 1: Producción por Operador (Barras horizontales)
with col1:
    st.subheader("Producción por Operador")
    operator_data = production_per_operator(df)
    
    fig1, ax1 = plt.subplots(figsize=(5, 6))
    fig1.patch.set_alpha(0)  # Fondo transparente
    ax1.patch.set_alpha(0)   # Fondo transparente
    
    colors1 = ['#00D9FF', '#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#A8E6CF']
    bars = ax1.barh(operator_data["Operador"], operator_data["Cantidad producida"], 
                    color=colors1[:len(operator_data)], height=0.6)
    
    # Agregar valores al final de las barras
    for i, (bar, value) in enumerate(zip(bars, operator_data["Cantidad producida"])):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2.,
                f' {int(value):,} L',
                ha='left', va='center', fontsize=9, fontweight='600', color='white')
    
    ax1.set_xlabel("Litros producidos", fontsize=11, color='white', fontweight='500')
    ax1.set_ylabel("Operador", fontsize=11, color='white', fontweight='500')
    ax1.tick_params(colors='#B0B0B0', labelsize=9)
    ax1.spines['bottom'].set_color('#404040')
    ax1.spines['left'].set_color('#404040')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.xaxis.grid(True, alpha=0.15, linestyle='-', linewidth=0.8, color='white')
    plt.tight_layout()
    st.pyplot(fig1, transparent=True)

# Gráfico 2: Producción por Tipo de Pintura
with col2:
    st.subheader("Producción por Tipo de Pintura")
    paint_data = total_per_paint(df)
    
    fig2, ax2 = plt.subplots(figsize=(5, 6))
    fig2.patch.set_alpha(0)  # Fondo transparente
    ax2.patch.set_alpha(0)   # Fondo transparente
    
    colors2 = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#A8E6CF', '#00D9FF']
    bars = ax2.bar(range(len(paint_data)), paint_data["Cantidad producida"], 
                   color=colors2[:len(paint_data)], width=0.6)
    
    # Agregar valores encima de las barras
    for bar, value in zip(bars, paint_data["Cantidad producida"]):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(value):,}',
                ha='center', va='bottom', fontsize=9, fontweight='600', color='white')
    
    ax2.set_xticks(range(len(paint_data)))
    ax2.set_xticklabels(paint_data["Tipo de pintura producida"], 
                        rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel("Litros producidos", fontsize=11, color='white', fontweight='500')
    ax2.tick_params(colors='#B0B0B0', labelsize=9)
    ax2.spines['bottom'].set_color('#404040')
    ax2.spines['left'].set_color('#404040')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.yaxis.grid(True, alpha=0.15, linestyle='-', linewidth=0.8, color='white')
    plt.tight_layout()
    st.pyplot(fig2, transparent=True)

# Gráfico 3: Distribución de Costos (Donut chart)
with col3:
    st.subheader("Costos por Tipo de Pintura")
    cost_data = total_cost_per_paint(df)
    
    fig3, ax3 = plt.subplots(figsize=(5, 6))
    fig3.patch.set_alpha(0)  # Fondo transparente
    
    colors3 = ['#4ECDC4', '#FF6B6B', '#95E1D3', '#FFE66D', '#A8E6CF', '#00D9FF']
    
    wedges, texts, autotexts = ax3.pie(
        cost_data["Costo de la producción"],
        labels=cost_data["Tipo de pintura producida"],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors3[:len(cost_data)],
        pctdistance=0.85,
        wedgeprops={'width': 0.5, 'edgecolor': 'none', 'linewidth': 0}
    )
    
    # Círculo central con transparencia
    centre_circle = plt.Circle((0, 0), 0.70, fc='#1E1E1E', linewidth=0, alpha=0.5)
    ax3.add_artist(centre_circle)
    
    # Mejorar el formato de los textos
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('600')
    
    for text in texts:
        text.set_fontsize(9)
        text.set_color('white')
        text.set_fontweight('500')
    
    ax3.text(0, 0, 'Costos\nTotales', ha='center', va='center', 
             fontsize=11, color='white', fontweight='600')
    
    plt.tight_layout()
    st.pyplot(fig3, transparent=True)


st.markdown("## Producción")
st.subheader("Información completa")
st.dataframe(df)


