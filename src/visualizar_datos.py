# visualizar_datos.py
import matplotlib.pyplot as plt
from conexion_bd import conectar_bd

def grafico_consumo_edad():
    db = conectar_bd()
    cursor = db.cursor()
    cursor.execute("SELECT edad, BebidasSemana FROM ENCUESTA")
    datos = cursor.fetchall()
    db.close()

    edades = [fila[0] for fila in datos]
    consumos = [fila[1] for fila in datos]

    plt.bar(edades, consumos)
    plt.xlabel('Edad')
    plt.ylabel('Bebidas por Semana')
    plt.title('Consumo de Bebidas por Edad')
    plt.show()
