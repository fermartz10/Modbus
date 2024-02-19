import threading
import time
import mysql.connector
import conexion


conexion.conectar_bd()

# Función para mostrar los datos de la tabla
def mostrar_datos_de_tabla(conn):
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM registros"
        cursor.execute(sql)
        resultados = cursor.fetchall()
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
        
        
def mostrar_datos_actualizados():
    while True:
        conexion_bd = conexion.conectar_bd()
        if conexion_bd is not None:
            mostrar_datos_de_tabla(conexion_bd)
            conexion_bd.close()
        else:
            print("No se pudo establecer conexión a la base de datos")
        time.sleep(10)  # Espera n segundos antes de la próxima actualización

def mostrar_datos():
    conexion_bd = conexion.conectar_bd()
    # Mostrar datos de la tabla
    if conexion_bd is not None:
        mostrar_datos_de_tabla(conexion_bd)
        conexion_bd.close()
    else:
        print("No se pudo establecer conexión a la base de datos")


def mostrar_actualizado():
    # Ejecutar la función mostrar_datos_actualizados en un hilo separado para que se actualice mientras se ejecuta el servidor Modbus
    threading.Thread(target=mostrar_datos_actualizados).start()
