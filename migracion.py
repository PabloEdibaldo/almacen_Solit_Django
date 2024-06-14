import csv
import mysql.connector
import datetime

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa238388$",
    database="solit"
)


# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Nombre del archivo CSV y nombre de la tabla en la base de datos
archivo_csv = 'INVENTARIO_2023.csv'
tabla_db = 'sistemaSolit_productos'

# Abrir el archivo CSV y leer los datos
with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.DictReader(archivo)
    
    # Iterar sobre cada fila del archivo CSV
    for fila in lector_csv:
        # Crear la consulta SQL para insertar los datos en la tabla
        consulta = f"INSERT INTO {tabla_db} (codigoInterno,zona,nombre_producto,observaciones,marca,modelo,stock,fecha_ingreso ) VALUES (%s, %s, %s,%s, %s, %s,%s,CURDATE())"
        
        # Ejecutar la consulta con los valores de la fila actual
        cursor.execute(consulta, (
            fila['CODIGO'],
            fila['UBICACION'],
            fila['PRODUCTO'], 
            fila['DESCRIPCION'],
            fila['MARCA'], 
            fila['MODELO'],
            fila['STOCK']))
    
    # Confirmar los cambios en la base de datos
    conexion.commit()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()


#
# 
#
   


"""
INSERT INTO sistemaSolit_usuario (nombre_completo, correo_electronico, numero_celular, equipo_trabajo, estatus, fecha_nacimiento, fotoPerfil, ubicacion, tipo_rol, password)
VALUES ('Pablo', 'pablo@gmail.com', '+521234567890', 'laptop', 1, CURDATE() , NULL, 'ubicacion_usuario', 'admin', 'pablo');
"""

