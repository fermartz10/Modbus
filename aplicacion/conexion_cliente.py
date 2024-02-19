import mysql.connector

def cliente_conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="192.168.0.9",
            user="root",  # Cambia esto al usuario de tu base de datos
            password="",  # Cambia esto a la contraseña de tu base de datos
            database="modbus_data"
        )
        print("Conexión exitosa a la base de datos MySQL")
        return conn
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos MySQL:", err)
        return None
