
## MENU EMPLEADOS ##

import pickle
import os
from tabulate import tabulate
from colorama import Fore, Style, init
init()

empleados_db = {}
NOMBRE_ARCHIVO_EMPLEADOS = "../datos/empleados.dat"
ultimo_codigo = 0


# Funciones de manejo de empleados 
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
        print(f"{Fore.RED}Error al cargar los datos de empleados: {e}")
        empleados_db = {}
        ultimo_codigo = 0
        
def guardar_empleados():
    try:
        with open(NOMBRE_ARCHIVO_EMPLEADOS, 'wb') as archivo:
            pickle.dump(empleados_db, archivo)
        print(f"Datos de empleados guardados en {NOMBRE_ARCHIVO_EMPLEADOS}")
    except Exception as e:
        print(f"{Fore.RED}Error al guardar los datos de empleados: {e}")

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
    empleados = empleados_db
    if empleados:
        # lista de tuplas con la información de los empleados
        empleados_lista = [
            (codigo, datos['nombre'], datos['cedula'], f"${datos['salario']:.2f}")
            for codigo, datos in empleados.items()
        ]
        
        # Tabla
        encabezado = [f"{Fore.CYAN}Código", f"{Fore.CYAN}Nombre", f"{Fore.CYAN}Cédula", f"{Fore.CYAN}Salario"]
        tabla = tabulate(empleados_lista, headers=encabezado, tablefmt="grid", numalign="center")
        
        # Mostrar la tabla
        print(f"\n{Fore.GREEN}📋 Lista de Todos los Empleados")
        print(tabla)
    else:
        print(f"{Fore.YELLOW}⚠️ No hay empleados registrados.")
        

## FUNCIONES DEL MENU ###
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "=" * 40)
    print("{:^40}".format(f"{Fore.MAGENTA}MENÚ DE GESTIÓN DE EMPLEADOS"))
    print("=" * 40)
    print(f"{Fore.GREEN}1. Registrar nuevo empleado")
    print(f"{Fore.GREEN}2. Consultar empleado por código")
    print(f"{Fore.GREEN}3. Listar todos los empleados")
    print(f"{Fore.GREEN}4. Actualizar información de un empleado")
    print(f"{Fore.GREEN}5. Eliminar empleado")
    print(f"{Fore.RED}6. Salir")
    print("=" * 40)

def pedir_datos_empleado():
    print("\n--- Ingrese los datos del empleado ---")
    nombre = input("Nombre completo: ").strip()
    cedula = input("Cédula: ").strip()
    while True:
        try:
            salario = float(input("Salario básico: "))
            if salario < 0:
                print(f"{Fore.RED}El salario no puede ser negativo.")
            else:
                break
        except ValueError:
            print(f"{Fore.RED}Por favor, ingrese un número válido para el salario.")
    return {
        "nombre": nombre,
        "cedula": cedula,
        "salario": salario
    }

def mostrar_empleado(codigo, datos):
    print("-" * 40)
    print(f"{Fore.CYAN}Código: {codigo}")
    print(f"{Fore.CYAN}Nombre: {datos['nombre']}")
    print(f"{Fore.CYAN}Cédula: {datos['cedula']}")
    print(f"{Fore.CYAN}Salario básico: ${datos['salario']:.2f}")
    print("-" * 40)

def menu():
    cargar_empleados()
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input(f"{Fore.YELLOW}Seleccione una opción: ").strip()

        if opcion == '1':
            limpiar_pantalla()
            datos = pedir_datos_empleado()
            codigo = agregar_empleado(datos)
            print(f"\n{Fore.GREEN}✅ Empleado registrado con código: {codigo}")

        elif opcion == '2':
            limpiar_pantalla()
            codigo = input(f"{Fore.YELLOW}Ingrese el código del empleado: ").strip()
            empleado = obtener_empleado(codigo)
            if empleado:
                print(f"\n{Fore.GREEN}📋 Información del Empleado")
                mostrar_empleado(codigo, empleado)
            else:
                print(f"{Fore.RED}❌ Empleado no encontrado.")

        elif opcion == '3':
            limpiar_pantalla()
            empleados = listar_empleados()
            if empleados:
                print("\n📋 Lista de Todos los Empleados")
                for codigo, datos in empleados.items():
                    mostrar_empleado(codigo, datos)
            else:
                print("⚠️ No hay empleados registrados.")

        elif opcion == '4':
            limpiar_pantalla()
            codigo = input("Código del empleado a actualizar: ").strip()
            empleado = obtener_empleado(codigo)
            if empleado:
                print("\n✏️ Datos actuales del empleado:")
                mostrar_empleado(codigo, empleado)
                print("\nIngrese los nuevos datos:")
                nuevos_datos = pedir_datos_empleado()
                actualizar_empleado(codigo, nuevos_datos)
                print("✅ Empleado actualizado correctamente.")
            else:
                print("❌ Empleado no encontrado.")

        elif opcion == '5':
            limpiar_pantalla()
            codigo = input("Código del empleado a eliminar: ").strip()
            confirmar = input(f"¿Está seguro que desea eliminar al empleado con código {codigo}? (s/n): ").lower()
            if confirmar == 's':
                if eliminar_empleado(codigo):
                    print(f"{Fore.GREEN}✅ Empleado eliminado correctamente.")
                else:
                    print(f"{Fore.RED}❌ Empleado no encontrado.")
            else:
                print("⏪ Operación cancelada.")

        elif opcion == '6':
            print("👋 Saliendo del sistema... ¡Hasta luego!")
            break

        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

        input("\nPresione ENTER para continuar...")
        
        
## Ejecutar
if __name__ == "__main__":
    menu()




