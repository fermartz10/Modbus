import tkinter as tk
from tkinter import ttk, messagebox
from pymodbus.server import StartTcpServer, ServerStop
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import threading
import mysql.connector
import conexion

class ModbusServerApp:
    def __init__(self, master):
        # Inicializa la aplicación de control del servidor Modbus.
        self.master = master
        master.title("Modbus Server Control")

        # Botones de la interfaz
        self.start_button = tk.Button(master, text="Iniciar Servidor", command=self.start_server)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Detener Servidor", command=self.stop_server)
        self.stop_button.pack()

        self.refresh_button = tk.Button(master, text="Actualizar Datos", command=self.show_database_data)
        self.refresh_button.pack()

        self.exit_button = tk.Button(master, text="Salir", command=self.exit_app)
        self.exit_button.pack()

        # Etiqueta y árbol para mostrar datos de la base de datos
        self.data_label = tk.Label(master, text="Datos de la Base de Datos:")
        self.data_label.pack()

        self.data_tree = ttk.Treeview(master, columns=("ID", "Valor"), show="headings")
        self.data_tree.heading("ID", text="ID")
        self.data_tree.heading("Valor", text="Valor")
        self.data_tree.pack()

        # Configuración del data store
        self.nreg = 200
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [15]*self.nreg),
            co=ModbusSequentialDataBlock(0, [16]*self.nreg),
            hr=ModbusSequentialDataBlock(0, [17]*self.nreg),
            ir=ModbusSequentialDataBlock(0, [18]*self.nreg))

    def start_server(self):
        # Inicia el servidor Modbus en un hilo separado.
        self.context = ModbusServerContext(slaves=self.store)
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'APMonitor'
        self.identity.ProductCode = 'APM'
        self.identity.VendorUrl = 'https://apmonitor.com'
        self.identity.ProductName = 'Modbus Server'
        self.identity.ModelName = 'Modbus Server'
        self.identity.MajorMinorRevision = '3.0.2'
        
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        # Ejecuta el servidor Modbus.
        try:
            StartTcpServer(context=self.context, identity=self.identity, address=("0.0.0.0", 502))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_server(self):
        # Detiene el servidor Modbus si está en ejecución.
        if hasattr(self, 'server_thread') and self.server_thread.is_alive():
            try:
                ServerStop()
                self.server_thread.join()
                messagebox.showinfo("Info", "Servidor detenido.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "El servidor no está en ejecución.")

    def exit_app(self):
        # Cierra la aplicación.
        if hasattr(self, 'server_thread') and self.server_thread.is_alive():
            self.stop_server()
        self.master.quit()

    def show_database_data(self):
    # Muestra los datos de la base de datos en el árbol de datos.
        try:
            conn = conexion.conectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registros")
            rows = cursor.fetchall()
            self.data_tree.delete(*self.data_tree.get_children())
            for row in rows:
                self.data_tree.insert("", tk.END, values=row)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error al conectar a la base de datos: " + str(e))


def main():
    root = tk.Tk()
    app = ModbusServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()