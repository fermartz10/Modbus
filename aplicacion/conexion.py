import mysql.connector

def crear_base_de_datos():
    try:
        # Establecer la conexión a MySQL (sin especificar la base de datos)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto al usuario de tu base de datos
            password="Holamundo150h"  # Cambia esto a la contraseña de tu base de datos
        )
        print("Conexión exitosa a MySQL")

        # Crear la base de datos "modbus_data" si no existe
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS modbus_data")
        cursor.execute("CREATE TABLE IF NOT EXISTS modbus_data.registros (id INT AUTO_INCREMENT PRIMARY KEY,valor VARCHAR(45) NULL)")
        print("Base de datos 'modbus_data' creada exitosamente")

    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos MySQL:", err)
    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Llamar a la función para crear la base de datos

def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto al usuario de tu base de datos
            password="Holamundo150h",  # Cambia esto a la contraseña de tu base de datos
            database="modbus_data"
        )
        print("Conexión exitosa a la base de datos MySQL")
        return conn
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos MySQL:", err)
        return None
