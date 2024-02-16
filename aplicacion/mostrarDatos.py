import mysql.connector
import conexion
import time


# Función para conectarse a la base de datos MySQL

conexion.conectar_bd()

# Función para mostrar los datos de la tabla
def mostrar_datos_de_tabla(conn):
    
    cursor = conn.cursor()
    try:
        # Consulta SQL para seleccionar todos los datos de la tabla
        sql = "SELECT * FROM registros"  # Cambia esto al nombre de tu tabla
        
        # Ejecutar la consulta SQL
        cursor.execute(sql)
        
        # Obtener todos los resultados de la consulta
        resultados = cursor.fetchall()
        
        # Imprimir los resultados
        if resultados:
            print("Datos en la tabla:")
            for fila in resultados:
                print(fila)
        else:
            print("No hay datos en la tabla")
    except mysql.connector.Error as err:
        print("Error al mostrar los datos de la tabla:", err)
    finally:
        cursor.close()
        

# Establecer conexión a la base de datos
conexion_bd = conexion.conectar_bd()

def mostrar_datos():
    # Mostrar datos de la tabla
    if conexion_bd is not None:
        mostrar_datos_de_tabla(conexion_bd)
        conexion_bd.close()
    else:
        print("No se pudo establecer conexión a la base de datos")
