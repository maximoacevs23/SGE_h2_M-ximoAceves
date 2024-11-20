# exportar_a_excel.py
import os
import pandas as pd
from sqlalchemy import create_engine

def exportar_a_excel():
    # Cambia 'CAMPUSFP' y 'tu_contraseña' por las credenciales correctas
    engine = create_engine("mysql+mysqlconnector://root:campusfp@localhost/ENCUESTAS")

    query = "SELECT * FROM ENCUESTA"
    df = pd.read_sql(query, engine)
    
    # Ruta donde se guardará el archivo exportado
    directorio_recursos = os.path.join(os.getcwd(), 'Excel Generado')
    
    # Asegúrate de que el directorio exista, si no, lo creas
    if not os.path.exists(directorio_recursos):
        os.makedirs(directorio_recursos)
    
    # Ruta completa para el archivo Excel
    ruta_archivo = os.path.join(directorio_recursos, 'encuestas_exportadas.xlsx')
    
    # Guardar el archivo Excel en el directorio 'recursos'
    df.to_excel(ruta_archivo, index=False)
    
    engine.dispose()  # Cerrar la conexión
