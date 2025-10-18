# Documentación Técnica
## Sistema de Dashboards de Producción para Mexicana de Pinturas Fake S.A. de C.V.

---

## 1. Resumen Ejecutivo

Este documento describe la arquitectura e implementación de un sistema automatizado de reportes de producción en la nube de AWS, diseñado para Mexicana de Pinturas Fake S.A. de C.V. El sistema permite la visualización de datos de producción diaria a través de dos dashboards especializados: uno gerencial (solo lectura del último reporte) y uno operativo (con filtros y consulta de históricos).

### 1.1 Objetivos del Proyecto
- Automatizar la generación de reportes de producción diaria
- Proporcionar visualización en tiempo real de datos de producción
- Permitir consulta de históricos de producción del año en curso
- Implementar seguridad mediante roles IAM de AWS
- Migrar de sistema basado en Excel a solución cloud escalable

---

## 2. Caso de Negocio

### 2.1 Problemática
Mexicana de Pinturas Fake S.A. de C.V. enfrentaba las siguientes limitaciones:
- Gestión manual de datos de producción en archivos Excel
- Falta de centralización de información histórica
- Imposibilidad de visualización en tiempo real
- Dificultad para análisis y toma de decisiones basada en datos

### 2.2 Solución Propuesta
Implementación de una arquitectura serverless en AWS que:
- Extrae datos automáticamente de la base de datos corporativa
- Procesa y transforma datos mediante funciones Lambda
- Almacena información en formato optimizado (Parquet)
- Presenta datos en dashboards interactivos mediante Streamlit
- Garantiza seguridad mediante autenticación IAM

---

## 3. Arquitectura del Sistema

### 3.1 Componentes Principales

#### 3.1.1 Seguridad
- **IAM Roles**: Control de acceso basado en roles
  - Permisos de ejecución para Lambdas
  - Acceso seguro a S3 y RDS desde EC2

#### 3.1.2 Origen de Datos
- **Amazon RDS (MySQL)**: Base de datos relacional que almacena producciones anteriores
- Contiene registros históricos de producción
- Conexión segura mediante VPC

#### 3.1.3 Procesamiento ETL

**Lambda 1 - Extracción (se ejecuta cada 24 hrs)**
- **Función**: Extracción de datos crudos
- **Trigger**: EventBridge (programación cada 24 horas)
- **Proceso**:
  1. Conecta a Amazon RDS
  2. Extrae datos de la última producción
  3. Convierte datos a formato CSV
  4. Deposita en S3 (`crudos/`)
- **Salida**: Archivo CSV con datos sin procesar

**Lambda 2 - Transformación**
- **Función**: Procesamiento y optimización de datos
- **Trigger**: Evento S3 (finalización exitosa de Lambda 1)
- **Proceso**:
  1. Lee el archivo CSV generado
  2. Aplica transformaciones:
     - Limpieza de datos
     - Normalización de formatos
     - Cálculos agregados
     - Validaciones de calidad
  3. Convierte a formato Parquet
  4. Organiza por estructura de carpetas: `produccion/YYYY-MM/produccion_YYYY-MM-DD.parquet`
- **Salida**: Archivo Parquet optimizado

#### 3.1.4 Almacenamiento
- **Amazon S3**: Almacenamiento de datos
  - **Bucket**: `xideralaws-curso-jonathan`
  - **Estructura de directorios**:
    ```
    /crudos/
      └── produccion_raw_YYYY-MM-DD.csv
    
    /produccion/
      └── YYYY-MM/
          └── produccion_YYYY-MM-DD.parquet
    ```

#### 3.1.5 Procesamiento AWS (Jupyter Notebook en EC2)
- **Función**: Procesamiento ETL de datos históricos
- **Uso**: Una sola ejecución para migrar datos anteriores a la implementación de RDS
- **Proceso**:
  1. Lee archivos Excel históricos
  2. Aplica transformaciones necesarias
  3. Genera archivos Parquet por fecha
  4. Deposita en S3 siguiendo estructura estándar

#### 3.1.6 Monitoreo
- **EventBridge**: Programación y monitoreo de ejecuciones
  - Trigger cada 24 horas para Lambda 1
  - Logs de ejecución
  

#### 3.1.7 Visualización
**Instancia EC2**
- **Sistema Operativo**: Ubuntu
- **Servicios ejecutándose**:
  - Dashboard Gerencial (puerto 8501)
  - Dashboard Operativo (puerto 8502)
- **Configuración**:
  - Auto-refresh cada 24 horas
  - Conexión directa a S3

**Dashboard Gerencial (EC2)**
- **Puerto**: 8501
- **Características**:
  - Solo visualización
  - Muestra última producción únicamente
  - Actualización automática cada 24 horas
  - Gráficos estáticos pero profesionales
  - KPIs principales en vista
- **Componentes visuales**:
  - Métricas: Fecha, Operadores, Tipos de pintura, Litros producidos, Costo total
  - Gráfico 1: Producción por operador (barras horizontales)
  - Gráfico 2: Producción por tipo de pintura (barras verticales)
  - Gráfico 3: Distribución de costos (gráfico donut)
  - Tabla: Información completa de producción

**Dashboard Operativo (EC2)**
- **Puerto**: 8502
- **Características**:
  - Interactivo con Plotly
  - Consulta de fechas pasadas (año en curso)
  - Filtros dinámicos:
    - Por operador
    - Por tipo de pintura
    - Por cantidad mínima producida
  - Búsqueda por fecha específica
  - Exportación de datos filtrados
- **Componentes visuales**:
  - Mismos gráficos que dashboard gerencial pero interactivos
  - Filtros en sidebar
  - Búsqueda por fecha personalizada
  - Tabla de datos filtrable

---

## 4. Flujo de Datos

### 4.1 Flujo de Producción Diaria (Automatizado)

```
1. EventBridge (trigger 24 hrs)
   ↓
2. Lambda 1 - Extracción
   - Conecta a RDS
   - Extrae última producción
   - Genera CSV
   - Guarda en S3 (origen de datos)
   ↓
3. S3 Event Trigger (éxito)
   ↓
4. Lambda 2 - Transformación
   - Lee CSV de S3
   - Aplica transformaciones
   - Convierte a Parquet
   - Guarda en S3 (produccion/YYYY-MM/)
   ↓
5. Dashboards (EC2)
   - Lee último archivo Parquet
   - Actualiza visualización
   - Usuarios acceden mediante navegador
```

### 4.2 Flujo de Consulta Histórica (Dashboard Operativo)

```
1. Usuario ingresa fecha en Dashboard Operativo
   ↓
2. Aplicación construye ruta: produccion/YYYY-MM/produccion_YYYY-MM-DD.parquet
   ↓
3. Descarga archivo desde S3
   ↓
4. Carga datos en memoria
   ↓
5. Aplica filtros seleccionados
   ↓
6. Renderiza visualizaciones
```

### 4.3 Flujo de Migración de Datos Históricos (Una sola ejecución)

```
1. Jupyter Notebook en EC2
   ↓
2. Lee archivos Excel históricos
   ↓
3. Procesa y transforma datos
   ↓
4. Genera archivos Parquet por fecha
   ↓
5. Deposita en S3 (produccion/YYYY-MM/)
```

---

## 5. Especificaciones Técnicas

### 5.1 Stack Tecnológico

**Infraestructura Cloud**
- AWS Lambda (Python 3.12)
- Amazon S3
- Amazon RDS (MySQL)
- Amazon EC2 (Ubuntu)
- AWS IAM
- Amazon EventBridge

**Lenguajes y Frameworks**
- Python 3.12
- Pandas (procesamiento de datos)
- Boto3 (SDK de AWS)
- PyArrow (formato Parquet en EC2)
- Streamlit (dashboards)
- Matplotlib (visualizaciones estáticas)
- Plotly (visualizaciones interactivas)

### 5.2 Estructura de Archivos Parquet

**Nomenclatura**: `produccion_YYYY-MM-DD.parquet`

**Schema de datos**:
```python
{
    "Fecha de producción": datetime64,
    "Tipo de pintura producida": string,
    "Cantidad producida": int64,
    "Costo por litro producido": float64,
    "Costo de la producción": float64,
    "Operador": string
}
```

**Organización**:
```
produccion/
├── 2025-01/
│   ├── produccion_2025-01-01.parquet
│   ├── produccion_2025-01-02.parquet
│   └── ...
├── 2025-02/
│   ├── produccion_2025-02-01.parquet
│   └── ...
└── 2025-MM/
    └── produccion_2025-MM-DD.parquet
```

### 5.3 Configuración de Servicios

#### Lambda 1 - Extracción
```yaml
Runtime: Python 3.12
Memory: 512 MB
Timeout: 5 minutes
Trigger: EventBridge (cron: 0 0 * * ? *)
Environment Variables:
  - DB_HOST: [RDS endpoint]
  - DB_NAME: produccion_db
  - BUCKET_NAME: xideralaws-curso-jonathan
IAM Role Permissions:
  - s3:GetObject
  - s3:PutObject
```

#### Lambda 2 - Transformación
```yaml
Runtime: Python 3.12
Memory: 1024 MB
Timeout: 10 minutes
Trigger: S3 Event (ObjectCreated)
Layers:
  - pandas
Environment Variables:
  - BUCKET_NAME: xideralaws-curso-jonathan
IAM Role Permissions:
  - s3:GetObject
  - s3:PutObject
  
```

#### EC2 - Dashboards
```yaml
Instance Type: t3.medium
vCPU: 2
Memory: 4 GB
Storage: 30 GB SSD
OS: Ubuntu 22.04 LTS
Security Group:
  - Inbound: 8501, 8502 (HTTP)
  - Outbound: 443 (HTTPS a S3)
IAM Role Permissions:
  - s3:GetObject
  - s3:ListBucket
Python Version: 3.12
Installed Packages:
  - streamlit
  - pandas
  - plotly
  - matplotlib
  - boto3
```

---
**Funciones principales**:
- `get_parquet(refresh_count)`: Carga datos desde S3
- `production_per_operator(df)`: Agrupa producción por operador
- `total_per_paint(df)`: Agrupa producción por tipo de pintura
- `total_cost_per_paint(df)`: Calcula costos por tipo de pintura

### 6 Dashboard Operativo

**Características adicionales**:
- Búsqueda por fecha específica
- Filtros dinámicos (multiselect)
- Slider para cantidad mínima
- Gráficos interactivos con Plotly
- Session state para mantener datos personalizados

### 6.1 Scripts Auxiliares

**last_folder.py**
```python
def get_last_folder_in_production(bucket_name, prefix='produccion/', specific_folder=None)
```
Obtiene la carpeta más reciente en S3 basándose en fecha de modificación.

**last_file.py**
```python
def get_last_file_in_folder(bucket_name, folder_path)
```
Obtiene el archivo más reciente dentro de una carpeta específica.

---


### 7 Beneficios Logrados
Automatización completa del proceso de reporteo  
Reducción de tiempo en generación de reportes de horas a minutos  
Visualización en tiempo real de datos de producción  
Consulta histórica eficiente  
Seguridad mediante IAM  
Escalabilidad para crecimiento futuro  
Reducción de costos vs soluciones on-premise  

---
