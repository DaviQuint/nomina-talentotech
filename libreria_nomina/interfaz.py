import os
from colorama import Fore, Style
from datetime import datetime
from utilidades import imprimir_tabla_empleado, imprimir_tabla_global
from empleados import agregar_empleado, listar_empleados, actualizar_empleado, obtener_empleado
from calculos import (
    calcular_salario_basico,
    calcular_auxilio_transporte,
    calcular_deduccion_salud,
    calcular_deduccion_pension,
    calcular_deducciones_totales,
    calcular_salario_bruto,
    calcular_salario_neto,
    calcular_totales_nomina
)
from libreria_nomina.validaciones import (validar_salario, validar_dias, validar_correo, validar_direccion, validar_nombre)
from libreria_nomina.graficos import generar_graficos, generar_pdf_reporte_empleados, generar_pdf_global
from libreria_nomina.constantes import SALARIO_MINIMO, AUXILIO_TRANSPORTE, DIAS_LABORALES_MES, CARPETA_REPORTES

MAX_LENGTH = 100

#La función devuelve el nombre del sistema operativo y luego dependiendo del sistema usa un comando para borrar la pantalla
def limpiarPantalla ():  
    if os.name == 'nt':  # Para sistemas Windows
        os.system('cls')
    else:  # Para sistemas Unix/Linux/Mac
        os.system('clear')

from libreria_nomina.validaciones import validar_nombre, validar_salario, validar_dias, validar_correo, validar_direccion
from libreria_nomina.constantes import MAX_LENGTH, SALARIO_MINIMO

def registrar_empleado():
    nombre = ""
    while not nombre:
        nombre = input(f"Nombre (máximo {MAX_LENGTH} caracteres): ")[:MAX_LENGTH]
        if not validar_nombre(nombre):
            print(Fore.RED + "Error: El nombre solo puede contener letras y espacios." + Style.RESET_ALL)
            nombre = ""  # Limpiar la variable para que el bucle continúe

    salario = None
    while salario is None:
        try:
            salario_str = input("Salario mensual: ")
            salario = float(salario_str)
            if not validar_salario(salario):
                print(Fore.RED + f"Error: El salario debe estar entre ${SALARIO_MINIMO} y $8,000,000." + Style.RESET_ALL)
                salario = None  # Resetear para que el bucle continúe
        except ValueError:
            print(Fore.RED + "Error: El salario debe ser un número." + Style.RESET_ALL)

    dias = None
    while dias is None:
        try:
            dias_str = input("Días trabajados: ")
            dias = int(dias_str)
            if not validar_dias(dias):
                print(Fore.RED + "Error: Número de días inválido (1-30)." + Style.RESET_ALL)
                dias = None  # Resetear para que el bucle continúe
        except ValueError:
            print(Fore.RED + "Error: Los días trabajados deben ser un número entero." + Style.RESET_ALL)

    direccion = ""
    while not direccion:
        direccion = input(f"Dirección (máximo {MAX_LENGTH} caracteres): ")[:MAX_LENGTH]
        if not validar_direccion(direccion):
            print(Fore.RED + "Error: La dirección no puede estar vacía." + Style.RESET_ALL)
            direccion = ""  # Limpiar la variable para que el bucle continúe

    correo = input(f"Correo electrónico (máximo {MAX_LENGTH} caracteres): ")[:MAX_LENGTH]
    if not validar_correo(correo):
        print(Fore.YELLOW + "Advertencia: Formato de correo electrónico inválido. Se guardará de todas formas." + Style.RESET_ALL)

    estado = "A"  # El estado siempre se establece como 'A' al crear

    datos = {
        "nombre": nombre,
        "salario": salario,
        "dias": dias,
        "direccion": direccion,
        "correo": correo,
        "estado": estado,
    }
    codigo_generado = agregar_empleado(datos)
    if codigo_generado:
        print(Fore.GREEN + f"Empleado registrado con código: {codigo_generado}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error al registrar el empleado." + Style.RESET_ALL)

def mostrar_empleados():
    empleados = listar_empleados()
    for codigo, datos in empleados.items():
        imprimir_tabla_empleado(codigo, datos)

def actualizar_info_empleado():
    codigo = input("Código del empleado a actualizar: ")
    empleado = obtener_empleado(codigo)
    if not empleado:
        print(Fore.RED + "Empleado no encontrado." + Style.RESET_ALL)
        return

    print("Deje vacío si no desea cambiar un valor.")

    nombre = input(f"Nuevo nombre ({empleado['nombre']}): ")[:MAX_LENGTH] or empleado['nombre']
    salario_str = input(f"Nuevo salario ({empleado['salario']}): ")
    salario = float(salario_str) if salario_str else empleado['salario']
    dias_str = input(f"Nuevos días trabajados ({empleado['dias']}): ")
    dias = int(dias_str) if dias_str else empleado['dias']
    direccion = input(f"Nueva dirección ({empleado.get('direccion', '')}): ")[:MAX_LENGTH] or empleado.get('direccion', '')
    correo = input(f"Nuevo correo electrónico ({empleado.get('correo', '')}): ")[:MAX_LENGTH] or empleado.get('correo', '')
    estado = input(f"Nuevo estado ({empleado.get('estado', 'A')} (A=Activo, I=Inactivo)): ").upper() or empleado.get('estado', 'A')
    if estado not in ["A", "I"]:
        print(Fore.RED + "Error: Estado inválido. Se mantendrá el estado actual." + Style.RESET_ALL)
        estado = empleado.get('estado', 'A')

    if not validar_nombre(nombre):
        print(Fore.RED + "Error: El nombre solo puede contener letras y espacios." + Style.RESET_ALL)
        return

    if not validar_salario(salario):
        print(Fore.RED + f"Error: El salario debe estar entre ${SALARIO_MINIMO} y $8,000,000." + Style.RESET_ALL)
        return

    if not validar_dias(dias):
        print(Fore.RED + "Error: Número de días inválido (1-30)." + Style.RESET_ALL)
        return

    if correo and not validar_correo(correo):
        print(Fore.RED + "Error: Formato de correo electrónico inválido." + Style.RESET_ALL)
        return

    if direccion and not validar_direccion(direccion):
        print(Fore.RED + "Error: La dirección no puede estar vacía." + Style.RESET_ALL)
        return

    nuevos_datos = {
        "nombre": nombre,
        "salario": salario,
        "dias": dias,
        "direccion": direccion,
        "correo": correo,
        "estado": estado,
    }

    if actualizar_empleado(codigo, nuevos_datos):
        print(Fore.GREEN + "Empleado actualizado." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error al actualizar el empleado." + Style.RESET_ALL)


def seleccionar_tipo_informe():
    print("\nSeleccione el tipo de informe a generar:")
    print("1. Gráfico de Histograma")
    print("2. Gráfico de Pastel")
    print("3. Gráfico de Líneas")
    print("4. PDF con tabla")
    print("5. Todos los anteriores")
    return input("Seleccione: ")

def generar_reportes():
    print(Fore.YELLOW + "\n=== GENERACIÓN DE REPORTES ===" + Style.RESET_ALL)
    print("1. Listado de empleados con salario, deducciones y neto (PDF)")
    print("2. Resumen de aportes a seguridad social (PDF)")
    print("3. Cálculo total de nómina a pagar")
    print("4. Gráficos estadísticos de pagos por mes (PDF - año actual)")
    opcion_reporte = input("Seleccione una opción: ")

    empleados = listar_empleados()
    if not empleados:
        print(Fore.RED + "No hay empleados registrados para generar reportes." + Style.RESET_ALL)
        return

    if opcion_reporte == "1":
        from libreria_nomina.graficos import generar_pdf_reporte_empleados
        generar_pdf_reporte_empleados(empleados, calcular_salario_basico, calcular_deducciones_totales, calcular_salario_neto)
        print(Fore.GREEN + "Reporte PDF de empleados generado en la carpeta 'reportes/'." + Style.RESET_ALL)
    elif opcion_reporte == "2":
        from libreria_nomina.graficos import generar_pdf_resumen_seguridad_social
        generar_pdf_resumen_seguridad_social(empleados, calcular_salario_basico, calcular_deduccion_salud, calcular_deduccion_pension)
        print(Fore.GREEN + "Resumen de aportes a seguridad social (PDF) generado en la carpeta 'reportes/'." + Style.RESET_ALL)
    elif opcion_reporte == "3":
        totales = calcular_totales_nomina(empleados)
        print(Fore.GREEN + "\n=== TOTAL DE NÓMINA A PAGAR ===" + Style.RESET_ALL)
        print(f"Total en Salario Neto a Pagar: ${totales['total_salario_neto']:,.2f}")
    elif opcion_reporte == "4":
        anio_actual = datetime.now().year
        from libreria_nomina.graficos import generar_pdf_graficos_pagos_mes
        generar_pdf_graficos_pagos_mes(empleados, calcular_salario_neto, anio_actual)
    else:
        print(Fore.RED + "Opción de reporte inválida." + Style.RESET_ALL)

def generar_liquidacion():
    print("\n¿Desea generar la liquidación de un solo empleado o de todos?")
    print("1. Individual")
    print("2. Global")
    tipo = input("Seleccione: ")

    opcion_informe = seleccionar_tipo_informe()

    print(Fore.CYAN + "\nResumen de selección de informe:")
    print(f"Tipo de informe: {'Individual' if tipo == '1' else 'Global'}")
    print("Contenido del informe:", end=" ")
    # ... (resto del bloque de selección de informe) ...

    if tipo == "1":
        codigo = input("Código del empleado: ")
        empleado = obtener_empleado(codigo)
        if not empleado:
            print(Fore.RED + "Empleado no encontrado." + Style.RESET_ALL)
            return

        salario_base = calcular_salario_basico(empleado["salario"], empleado["dias"])
        auxilio = calcular_auxilio_transporte(empleado["salario"], empleado["dias"])
        deducciones = calcular_deducciones_totales(salario_base) # Usamos las totales
        salario_bruto = calcular_salario_bruto(salario_base, auxilio)
        salario_neto = calcular_salario_neto(salario_bruto, deducciones)

        datos_liquidacion = { # Modificamos los datos a mostrar
            "Salario Básico": salario_base,
            "Auxilio Transporte": auxilio,
            "Deducción Salud": calcular_deduccion_salud(salario_base),
            "Deducción Pensión": calcular_deduccion_pension(salario_base),
            "Deducciones Totales": deducciones,
            "Salario Bruto": salario_bruto,
            "Salario Neto": salario_neto
        }

        imprimir_tabla_empleado(codigo, empleado, datos_liquidacion)

        if opcion_informe in ["1", "2", "3", "5"]:
            tipo_grafico = {
                "1": "barras",
                "2": "pastel",
                "3": "lineas",
                "5": "todos"
            }.get(opcion_informe, "barras")
            generar_graficos(datos_liquidacion, empleado["nombre"], tipo_grafico)

        if opcion_informe in ["4", "5"]:
            generar_pdf_reporte_empleados(empleado["nombre"], datos_liquidacion)

        print(Fore.GREEN + "Informe individual generado en la carpeta 'reportes/'." + Style.RESET_ALL)

    elif tipo == "2":
        empleados = listar_empleados()
        imprimir_tabla_global(
            empleados,
            calcular_salario_basico,
            calcular_auxilio_transporte,
            calcular_deduccion_salud,
            calcular_deduccion_pension,
            calcular_deducciones_totales,
            calcular_salario_bruto,
            calcular_salario_neto
        )

        totales = calcular_totales_nomina(empleados)
        print(Fore.GREEN + "\n=== TOTALES GENERALES ===" + Style.RESET_ALL)
        print(f"Total Gastado en Salud: ${totales['total_salud']:,.2f}")
        print(f"Total Gastado en Pensión: ${totales['total_pension']:,.2f}")
        print(f"Total Pagado en Auxilio de Transporte: ${totales['total_auxilio_transporte']:,.2f}")
        print(f"Total en Salario Bruto: ${totales['total_salario_bruto']:,.2f}")
        print(f"Total en Salario Neto Pagado: ${totales['total_salario_neto']:,.2f}")

        if opcion_informe in ["4", "5"]:
            generar_pdf_global(
                empleados,
                calcular_salario_basico,
                calcular_auxilio_transporte,
                calcular_deduccion_salud,
                calcular_deduccion_pension,
                calcular_deducciones_totales,
                calcular_salario_bruto,
                calcular_salario_neto
            )
            print(Fore.GREEN + "Informe global generado en la carpeta 'reportes/'." + Style.RESET_ALL)

        if opcion_informe in ["1", "2", "3", "5"]:
            tipo_grafico = {
                "1": "barras",
                "2": "pastel",
                "3": "lineas",
                "5": "todos"
            }.get(opcion_informe, "barras")

            for codigo, datos in empleados.items():
                salario_base = calcular_salario_basico(datos["salario"], datos["dias"])
                auxilio = calcular_auxilio_transporte(datos["salario"], datos["dias"])
                deducciones = calcular_deducciones_totales(salario_base)
                salario_bruto = calcular_salario_bruto(salario_base, auxilio)
                salario_neto = calcular_salario_neto(salario_bruto, deducciones)
                info_grafico = {
                    "Salario Básico": salario_base,
                    "Auxilio Transporte": auxilio,
                    "Deducciones Totales": deducciones,
                    "Salario Neto": salario_neto
                }
                generar_graficos(info_grafico, datos["nombre"], tipo_grafico)

    else:
        print(Fore.RED + "Opción inválida." + Style.RESET_ALL)

# ... (importaciones)
from libreria_nomina.empleados import agregar_empleado, listar_empleados, actualizar_empleado, obtener_empleado, eliminar_empleado, cargar_empleados, guardar_empleados

def menu_principal():
    limpiarPantalla()
    cargar_empleados()  
    while True:
        print(Fore.YELLOW + "\n=== MENÚ PRINCIPAL ===" + Style.RESET_ALL)
        print("1. Registrar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Generar liquidación")
        print("6. Generar reportes")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            limpiarPantalla()
            registrar_empleado()
        elif opcion == "2":
            limpiarPantalla()
            mostrar_empleados()
        elif opcion == "3":
            limpiarPantalla()
            actualizar_info_empleado()
        elif opcion == "4":
            limpiarPantalla()
            eliminar_empleado_interfaz()
        elif opcion == "5":
            limpiarPantalla()
            generar_liquidacion() # Aquí se mantiene la generación individual/global con gráficos individuales
        elif opcion == "6":
            limpiarPantalla()
            generar_reportes()  # Llama a la nueva función para los reportes específicos
        elif opcion == "7":
            limpiarPantalla()
            guardar_empleados() # Guardar los datos antes de salir
            print(Fore.BLUE + "Gracias por usar el sistema de nómina." + Style.RESET_ALL)
            break
        else:
            limpiarPantalla()
            print(Fore.RED + "Opción inválida." + Style.RESET_ALL)

def eliminar_empleado_interfaz():
    codigo = input("Código del empleado a eliminar: ")
    if eliminar_empleado(codigo): # Llama a la función del módulo empleados
        print(Fore.GREEN + f"Empleado con código {codigo} eliminado." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No se encontró ningún empleado con el código {codigo}." + Style.RESET_ALL)