import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import pandas as pd
import subprocess
import boto3
import io
from last_folder import get_last_folder_in_production
from last_file import get_last_file_in_folder

st.set_page_config(page_title="Dashboard Operativo", layout="wide")
count = st_autorefresh(interval=60000, limit=None, key="datarefresh_operativo")

# Función para actualizar datos operativos
def update_operativo_data():
    try:
        BUCKET_NAME = "xideralaws-curso-jonathan"
        carpeta = get_last_folder_in_production(BUCKET_NAME)
        path = f"produccion/{carpeta}"
        file = get_last_file_in_folder(BUCKET_NAME, path)
        
        # Construir ruta completa del parquet
        parquet_key = f"{path}{file}"
        
        # Leer parquet desde S3
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=parquet_key)
        parquet_buffer = io.BytesIO(obj['Body'].read())
        df = pd.read_parquet(parquet_buffer)
        
        # Guardar como CSV con nombre específico
        #output_csv = "datos_operativo.csv"
        #df.to_csv(output_csv, index=False)
        
        return df
    except Exception as e:
        st.error(f"Error al actualizar datos: {str(e)}")
        return None

# Función para cargar datos
@st.cache_data(ttl=60)
def load_operativo_data():
    try:
        return pd.read_csv("datos_operativo.csv", encoding='utf-8')
    except:
        return None

# Actualizar datos
df_temp = update_operativo_data()
if df_temp is not None:
    df = df_temp
else:
    # Si falla, intentar cargar el CSV existente
    df = load_operativo_data()
    if df is None:
        st.error("No se pudieron cargar los datos")
        st.stop()

# Sidebar con filtros
st.sidebar.title("Filtros")
st.sidebar.markdown("---")

# Búsqueda por fecha específica
st.sidebar.subheader("Buscar por Fecha")
fecha_input = st.sidebar.text_input(
    "Fecha (YYYY-MM-DD)",
    placeholder="2025-10-18",
    key="fecha_operativo"
)

if st.sidebar.button("Buscar Producción", use_container_width=True, key="buscar_operativo"):
    if fecha_input:
        try:
            # Validar y parsear la fecha
            fecha_obj = pd.to_datetime(fecha_input, format="%Y-%m-%d")
            
            # Formatear fecha para obtener año-mes y fecha completa
            yyyy_mm = fecha_obj.strftime("%Y-%m")
            yyyy_mm_dd = fecha_obj.strftime("%Y-%m-%d")
            
            # Construir ruta del archivo
            folder_path = f"produccion/{yyyy_mm}/"
            file_name = f"produccion_{yyyy_mm_dd}.parquet"
            full_path = f"{folder_path}{file_name}"
            
            st.sidebar.info(f"Buscando: {full_path}")
            
            # Cargar archivo específico desde S3
            BUCKET_NAME = "xideralaws-curso-jonathan"
            s3 = boto3.client('s3')
            
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=full_path)
            parquet_buffer = io.BytesIO(obj['Body'].read())
            df = pd.read_parquet(parquet_buffer)
            
            # Guardar en session_state para mantener los datos
            st.session_state['df_custom_operativo'] = df
            st.sidebar.success(f"Datos cargados: {len(df)} registros")
            
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")
            st.sidebar.warning("Verifica que la fecha tenga datos disponibles")
    else:
        st.sidebar.warning("Por favor selecciona una fecha")

st.sidebar.markdown("---")

# Determinar qué DataFrame usar
if 'df_custom_operativo' in st.session_state and st.session_state['df_custom_operativo'] is not None:
    df = st.session_state['df_custom_operativo']
    st.sidebar.info("Mostrando datos personalizados")
    if st.sidebar.button("Volver a datos actuales", key="volver_operativo"):
        del st.session_state['df_custom_operativo']
        st.rerun()
else:
    update_operativo_data()
    df = load_operativo_data()
    st.sidebar.info("Mostrando datos más recientes")

st.sidebar.markdown("---")

selected_operators = st.sidebar.multiselect(
    "Operadores",
    options=df["Operador"].unique(),
    default=df["Operador"].unique(),
    key="operators_operativo"
)

selected_paints = st.sidebar.multiselect(
    "Tipos de Pintura",
    options=df["Tipo de pintura producida"].unique(),
    default=df["Tipo de pintura producida"].unique(),
    key="paints_operativo"
)

min_quantity = st.sidebar.slider(
    "Cantidad Mínima Producida",
    min_value=int(df["Cantidad producida"].min()),
    max_value=int(df["Cantidad producida"].max()),
    value=int(df["Cantidad producida"].min()),
    key="quantity_operativo"
)

st.sidebar.markdown("---")
st.sidebar.info(f"Actualizaciones: {count}")

# Filtrar datos
df_filtered = df[
    (df["Operador"].isin(selected_operators)) &
    (df["Tipo de pintura producida"].isin(selected_paints)) &
    (df["Cantidad producida"] >= min_quantity)
]

# Dashboard principal
st.title("Mexicana de pinturas fake S.A. de C.V.")

# KPIs
if len(df_filtered) > 0:
    date = pd.to_datetime(df_filtered["Fecha de producción"].iloc[0]).strftime("%Y-%m-%d")
else:
    date = "N/A"
operators = df_filtered["Operador"].nunique()
paints = df_filtered["Tipo de pintura producida"].nunique()
total_quantity = df_filtered["Cantidad producida"].sum()
cost = df_filtered["Costo de la producción"].sum()

# Métricas
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Fecha", date)
col2.metric("Operadores", operators)
col3.metric("Tipos de Pintura", paints)
col4.metric("Litros Producidos", f"{total_quantity:,}")
col5.metric("Costo Total", f"${cost:,.2f}")

st.divider()

# Gráficos interactivos
col1, col2, col3 = st.columns(3)

# Gráfico 1: Producción por Operador
with col1:
    st.subheader("Producción por Operador")
    operator_data = df_filtered.groupby("Operador", as_index=False)["Cantidad producida"].sum()
    
    fig1 = go.Figure(data=[go.Bar(
        y=operator_data["Operador"],
        x=operator_data["Cantidad producida"],
        orientation='h',
        marker=dict(
            color=['#00D9FF', '#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#A8E6CF'][:len(operator_data)],
            line=dict(color='white', width=2)
        ),
        text=operator_data["Cantidad producida"],
        texttemplate='%{text:,} L',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Producción: %{x:,} L<extra></extra>'
    )])
    
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(title="Litros Producidos", gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        yaxis=dict(title="Operador"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Producción por Tipo de Pintura
with col2:
    st.subheader("Producción por Tipo de Pintura")
    paint_data = df_filtered.groupby("Tipo de pintura producida", as_index=False)["Cantidad producida"].sum().sort_values(by="Cantidad producida", ascending=False)
    
    fig2 = go.Figure(data=[go.Bar(
        x=paint_data["Tipo de pintura producida"],
        y=paint_data["Cantidad producida"],
        marker=dict(
            color=['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#A8E6CF', '#00D9FF'][:len(paint_data)],
            line=dict(color='white', width=2)
        ),
        text=paint_data["Cantidad producida"],
        texttemplate='%{text:,}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Producción: %{y:,} L<extra></extra>'
    )])
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(title="Tipo de Pintura", tickangle=-45),
        yaxis=dict(title="Litros Producidos", gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Distribución de Costos
with col3:
    st.subheader("Costos por Tipo de Pintura")
    cost_data = df_filtered.groupby("Tipo de pintura producida", as_index=False)["Costo de la producción"].sum()
    
    fig3 = go.Figure(data=[go.Pie(
        labels=cost_data["Tipo de pintura producida"],
        values=cost_data["Costo de la producción"],
        hole=0.5,
        marker=dict(
            colors=['#4ECDC4', '#FF6B6B', '#95E1D3', '#FFE66D', '#A8E6CF', '#00D9FF'][:len(cost_data)],
            line=dict(color='white', width=2)
        ),
        textposition='outside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Costo: $%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=11),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        showlegend=False,
        annotations=[dict(
            text='Costos<br>Totales',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False,
            font=dict(color='white')
        )],
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Tabla de datos
st.markdown("Información Completa")
df_display = df_filtered.copy()
df_display["Fecha de producción"] = pd.to_datetime(df_display["Fecha de producción"]).dt.strftime("%Y-%m-%d")
st.dataframe(df_display, use_container_width=True, height=400)