
import mysql.connector
import conexion_cliente

conexion_cliente.cliente_conectar_bd()

# Función para guardar los datos en la base de datos
def guardar_datos_en_bd(data):
    conn = conexion_cliente.cliente_conectar_bd()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        for d in data:
            cursor.execute("INSERT INTO registros (valores) VALUES (%s)", (d,))
        conn.commit()
        print("Datos guardados en la base de datos exitosamente")
    except mysql.connector.Error as err:
        print("Error al guardar los datos en la base de datos:", err)
    finally:
        cursor.close()
        conn.close()