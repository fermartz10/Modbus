import tkinter as tk
from tkinter import messagebox
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import guardarDatos
import time

def conectar_servidor():
    direccion_ip = entrada_ip.get()
    try:
        client = ModbusClient(host=direccion_ip, port=502)
        client.connect()
        messagebox.showinfo("Conexión exitosa", "Conexión al servidor Modbus exitosa")
        leer_registros(client)
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor Modbus: {e}")

def leer_registros(client):
    reg = 0
    address = 0
    data = [0.1, 1.1, 2.1, 3.1, 4.1]
    numero_ciclo = 0
    for i in range(10):
        numero_ciclo = numero_ciclo + 1
        time.sleep(1.0)
        for i, d in enumerate(data):
            data[i] = d + 1
            

        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        for d in data:
            builder.add_16bit_int(int(d))
        payload = builder.build()
        result = client.write_registers(int(reg), payload, skip_encode=True, unit=int(address))

        rd = client.read_holding_registers(reg, len(data)).registers
        texto_registros.insert(tk.END, f"Ciclo {numero_ciclo}: {rd}\n")
        guardarDatos.guardar_datos_en_bd(rd)

def salir_aplicacion():
    ventana.destroy()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Conexión")
ventana.geometry("400x300")

etiqueta_ip = tk.Label(ventana, text="Dirección IP del servidor:")
etiqueta_ip.pack()

entrada_ip = tk.Entry(ventana)
entrada_ip.pack()

boton_conectar = tk.Button(ventana, text="Conectar al servidor", command=conectar_servidor)
boton_conectar.pack(pady=10)

texto_registros = tk.Text(ventana, height=10, width=50)
texto_registros.pack()

boton_salir = tk.Button(ventana, text="Salir", command=salir_aplicacion)
boton_salir.pack()

ventana.mainloop()

