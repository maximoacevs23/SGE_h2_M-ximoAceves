import mysql.connector
from mysql.connector import Error

def conectar_bd():
    """
    Establece y devuelve una conexión a la base de datos MySQL.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="campusfp",
            database="ENCUESTAS"
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

