"""
Módulo: conexion_base_de_datos.py

Este módulo contiene la función necesaria para establecer conexión con la base de datos MySQL
utilizada en el sistema SkyRoute S.A.

La configuración de conexión (host, usuario, contraseña, base de datos, etc.) se importa
desde el módulo 'config.py'.
"""

import mysql.connector
from config import config


def obtener_conexion():
    """
    Establece una conexión con la base de datos MySQL utilizando los parámetros definidos en 'config.py'.

    Returns:
        mysql.connector.connection.MySQLConnection | None: 
            Objeto de conexión activo si la conexión fue exitosa, o None si falló.
    """
    try:
        conexion = mysql.connector.connect(**config)
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None


if __name__ == "__main__":
    # Test de conexión (modo diagnóstico)
    conexion = obtener_conexion()
    if conexion:
        print("Conexión exitosa.")
        conexion.close()
    else:
        print("No se pudo conectar.")
