
# Módulo para manejo CRUD de empleados

import pickle
import os
import re  # Importar el módulo para expresiones regulares

empleados_db = {}
NOMBRE_ARCHIVO_EMPLEADOS = "../datos/empleados.dat"
ultimo_codigo = 0

def cargar_empleados():
    global empleados_db, ultimo_codigo
    try:
        with open(NOMBRE_ARCHIVO_EMPLEADOS, 'rb') as archivo:
            empleados_db = pickle.load(archivo)
        print(f"Datos de empleados cargados desde {NOMBRE_ARCHIVO_EMPLEADOS}")
        if empleados_db:
            ultimo_codigo = max(int(codigo) for codigo in empleados_db.keys())
        else:
            ultimo_codigo = 0
    except FileNotFoundError:
        print(f"Archivo {NOMBRE_ARCHIVO_EMPLEADOS} no encontrado. Se iniciará con una base de datos de empleados vacía.")
        empleados_db = {}
        ultimo_codigo = 0
    except Exception as e:
        print(f"Error al cargar los datos de empleados: {e}")
        empleados_db = {}
        ultimo_codigo = 0

def guardar_empleados():
    try:
        with open(NOMBRE_ARCHIVO_EMPLEADOS, 'wb') as archivo:
            pickle.dump(empleados_db, archivo)
        print(f"Datos de empleados guardados en {NOMBRE_ARCHIVO_EMPLEADOS}")
    except Exception as e:
        print(f"Error al guardar los datos de empleados: {e}")

def agregar_empleado(datos): # El código ya no es un parámetro
    global ultimo_codigo
    ultimo_codigo += 1
    codigo = str(ultimo_codigo).zfill(3) # Formatear con ceros iniciales si se desea
    empleados_db[codigo] = datos
    guardar_empleados()
    return codigo # Devolver el código generado

def obtener_empleado(codigo):
    return empleados_db.get(codigo)

def actualizar_empleado(codigo, nuevos_datos):
    if codigo in empleados_db:
        empleados_db[codigo].update(nuevos_datos)  # Usar update para modificar solo los campos proporcionados
        guardar_empleados()
        return True
    return False

def eliminar_empleado(codigo):
    if codigo in empleados_db:
        del empleados_db[codigo]
        guardar_empleados()
        return True
    return False

def listar_empleados():
    return empleados_db


cargar_empleados()