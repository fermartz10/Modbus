import tkinter as tk
from tkinter import ttk
import mysql.connector
import conexion

# Función para conectar a la base de datos
conexion.conectar_bd

# Función para obtener los datos de la tabla
def obtener_datos():
    conn = conexion.conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM registros")
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta:", err)
        finally:
            cursor.close()
            conn.close()

# Función para mostrar los datos en la ventana
def mostrar_datos():
    resultados = obtener_datos()
    if resultados:
        for fila in tree.get_children():
            tree.delete(fila)
        for fila in resultados:
            tree.insert("", "end", values=fila)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz de Base de Datos")

# Crear el Treeview
tree = ttk.Treeview(root, columns=("ID", "Valor")) # Ajusta el número de columnas según tu tabla
tree.heading("#0", text="ID")
tree.heading("#1", text="Valor")  # Reemplaza "Nombre" con el nombre real de la columna
tree.pack(fill="both", expand=True)

# Botón para mostrar los datos
mostrar_button = tk.Button(root, text="Mostrar Datos", command=mostrar_datos)
mostrar_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()