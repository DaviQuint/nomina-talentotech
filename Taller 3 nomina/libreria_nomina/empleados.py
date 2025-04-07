
# Módulo para manejo CRUD de empleados

empleados_db = {}

def agregar_empleado(codigo, datos):
    empleados_db[codigo] = datos

def obtener_empleado(codigo):
    return empleados_db.get(codigo)

def actualizar_empleado(codigo, nuevos_datos):
    if codigo in empleados_db:
        empleados_db[codigo] = nuevos_datos
        return True
    return False

def eliminar_empleado(codigo):
    return empleados_db.pop(codigo, None)

def listar_empleados():
    return empleados_db
