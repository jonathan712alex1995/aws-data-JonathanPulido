import mysql.connector
import pandas as pd

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

