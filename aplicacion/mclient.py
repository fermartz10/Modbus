from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import mysql.connector
import time
import conexion

conexion.conectar_bd()

# Función para guardar los datos en la base de datos
def guardar_datos_en_bd(data):
    conn = conexion.conectar_bd()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        for d in data:
            cursor.execute("INSERT INTO registros (valor) VALUES (%s)", (d,))
        conn.commit()
        print("Datos guardados en la base de datos exitosamente")
    except mysql.connector.Error as err:
        print("Error al guardar los datos en la base de datos:", err)
    finally:
        cursor.close()
        conn.close()


'''def obtener_direccion_ip():
    while True:
        direccion_ip = input("Por favor, ingresa la dirección IP: ")
        # Validar la dirección IP ingresada
        if validar_direccion_ip(direccion_ip):
            return direccion_ip
        else:
            print("Dirección IP no válida. Por favor, inténtalo de nuevo.")

def validar_direccion_ip(direccion_ip):
    partes = direccion_ip.split('.')
    # Una dirección IP válida tiene 4 partes separadas por puntos
    if len(partes) != 4:
        return False
    # Cada parte debe ser un número entre 0 y 255
    for parte in partes:
        if not (0 <= int(parte) <= 255):
            return False
    return True'''



# Ejemplo de uso
#direccion_ip = obtener_direccion_ip()
print('Start Modbus Client')
client = ModbusClient(host='127.0.0.1', port=502)
reg=0; address=0

# initialize data
data = [0.1,1.1,2.1,3.1,4.1]

for i in range(10):
    print('-'*5,'Cycle ',i,'-'*30)
    time.sleep(1.0)

   # increment data by one
    for i,d in enumerate(data):
      data[i] = d + 1

   # write holding registers (40001 to 40005)
    print('Write',data)
    builder = BinaryPayloadBuilder(byteorder = Endian.BIG, 
                                   wordorder = Endian.LITTLE)
    
    for d in data:
      builder.add_16bit_int(int(d))
    payload = builder.build()
    result  = client.write_registers(int(reg), payload,\
              skip_encode=True, unit=int(address))

   # read holding registers
    rd = client.read_holding_registers(reg,len(data)).registers
    print('Read',rd)
    
    # Guardar los datos en la base de datos
    guardar_datos_en_bd(data)

client.close()