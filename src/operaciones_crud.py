

from conexion_bd import conectar_bd
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="campusfp",
    database="ENCUESTAS"
)






def agregar_encuesta(edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, 
                     bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia, problemas_digestivos, tension_alta, dolor_cabeza):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, 
            BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, 
              bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia, problemas_digestivos, tension_alta, dolor_cabeza))
        conn.commit()
        print("Encuesta agregada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al agregar encuesta: {err}")




def mostrar_encuestas(text_widget):
    """
    Muestra todas las encuestas almacenadas en la base de datos en un widget de texto.
    """
    encuestas = leer_encuestas()
    campos = [
        "ID de Encuesta: Identificador único.",
        "Edad: Edad del encuestado en años.",
        "Sexo: Género del encuestado.",
        "Bebidas por Semana: Cantidad de bebidas alcohólicas consumidas en una semana.",
        "Cervezas por Semana: Número de cervezas consumidas en una semana.",
        "Bebidas Fin de Semana: Bebidas alcohólicas consumidas en los fines de semana.",
        "Bebidas Destiladas por Semana: Cantidad de bebidas destiladas consumidas por semana.",
        "Vinos por Semana: Cantidad de vino consumido por semana.",
        "Pérdidas de Control: Número de ocasiones en las que el encuestado ha perdido el control debido al alcohol.",
        "Diversión Dependencia Alcohol: Si el encuestado asocia el alcohol con diversión (SI/NO).",
        "Problemas Digestivos: Si el encuestado tiene problemas digestivos debido al alcohol (SI/NO).",
        "Tensión Alta: Si el encuestado tiene tensión alta (SI/NO).",
        "Dolores de Cabeza: Si el encuestado experimenta dolores de cabeza debido al alcohol (SI/NO)."
    ]
    text_widget.delete(1.0, tk.END)  # Limpiar la caja de texto antes de mostrar las encuestas

    for encuesta in encuestas:
        texto = "\n".join([f"{campo}: {valor}" for campo, valor in zip(campos, encuesta)])
        text_widget.insert(tk.END, texto + "\n\n")

def leer_encuestas():
    """
    Lee todas las encuestas desde la base de datos.
    """
    db = conectar_bd()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ENCUESTA")
    encuestas = cursor.fetchall()
    db.close()
    return encuestas

def eliminar_encuesta(id_encuesta):
    """
    Elimina una encuesta de la base de datos por su ID.
    """
    db = conectar_bd()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta = %s", (id_encuesta,))
    db.commit()
    db.close()


def actualizar_encuesta(id_encuesta, num_columna, nuevo_valor):
    """
    Actualiza una encuesta en la base de datos utilizando un número de columna.
    """
    # Mapeo de número a columna (excluyendo 'idEncuesta')
    columnas = [
        "edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", 
        "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", 
        "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
    ]
    
    # Asegurarse de que num_columna sea un entero
    try:
        num_columna = int(num_columna)  # Convertir a entero
    except ValueError:
        print(f"Error: '{num_columna}' no es un número válido.")
        return

    # Verificar si el número de columna está dentro del rango (excluyendo 'idEncuesta')
    if num_columna < 1 or num_columna > 12:  # El rango válido es del 1 al 12
        print(f"Error: El número de columna '{num_columna}' no es válido.")
        return

    columna = columnas[num_columna - 1]  # Ajustar el índice (restando 1 para que 1 corresponda a 'edad')

    try:
        db = conectar_bd()
        cursor = db.cursor()

        # Comprobación de tipo para nuevo_valor (si es necesario convertir a entero para algunas columnas)
        if columna in ["edad", "CervezasSemana", "BebidasDestiladasSemana", "VinosSemana"]:
            nuevo_valor = int(nuevo_valor)
        
        # Ejecutar la consulta SQL
        cursor.execute(f"UPDATE ENCUESTA SET {columna} = %s WHERE idEncuesta = %s", (nuevo_valor, id_encuesta))
        db.commit()

        print("Encuesta actualizada correctamente.")
        
    except mysql.connector.Error as err:
        print(f"Error al actualizar encuesta: {err}")
    finally:
        # Asegurarse de cerrar la conexión incluso si ocurre un error
        if db.is_connected():
            db.close()
