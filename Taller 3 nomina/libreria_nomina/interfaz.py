from colorama import Fore, Style
from libreria_nomina.utilidades import imprimir_tabla_empleado, imprimir_tabla_global
from libreria_nomina.empleados import agregar_empleado, listar_empleados, actualizar_empleado, obtener_empleado
from libreria_nomina.calculos import calcular_salario_basico, calcular_auxilio_transporte, calcular_deducciones, calcular_total_pago
from libreria_nomina.validaciones import validar_salario, validar_dias
from libreria_nomina.graficos import generar_graficos, generar_pdf_empleado, generar_pdf_global

def registrar_empleado():
    codigo = input("Código del empleado: ")
    nombre = input("Nombre: ")
    salario = float(input("Salario mensual: "))
    dias = int(input("Días trabajados: "))

    if not validar_salario(salario):
        print(Fore.RED + "Error: El salario no puede ser menor al salario mínimo." + Style.RESET_ALL)
        return

    if not validar_dias(dias):
        print(Fore.RED + "Error: Número de días inválido." + Style.RESET_ALL)
        return

    datos = {
        "nombre": nombre,
        "salario": salario,
        "dias": dias
    }

    agregar_empleado(codigo, datos)
    print(Fore.GREEN + "Empleado registrado con éxito." + Style.RESET_ALL)

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

    nombre = input(f"Nuevo nombre ({empleado['nombre']}): ") or empleado['nombre']
    salario = input(f"Nuevo salario ({empleado['salario']}): ")
    salario = float(salario) if salario else empleado['salario']
    dias = input(f"Nuevos días trabajados ({empleado['dias']}): ")
    dias = int(dias) if dias else empleado['dias']

    if not validar_salario(salario) or not validar_dias(dias):
        print(Fore.RED + "Datos inválidos." + Style.RESET_ALL)
        return

    nuevos_datos = {
        "nombre": nombre,
        "salario": salario,
        "dias": dias
    }

    actualizar_empleado(codigo, nuevos_datos)
    print(Fore.GREEN + "Empleado actualizado." + Style.RESET_ALL)

def seleccionar_tipo_informe():
    print("\nSeleccione el tipo de informe a generar:")
    print("1. Gráfico de Histograma")
    print("2. Gráfico de Pastel")
    print("3. Gráfico de Líneas")
    print("4. PDF con tabla")
    print("5. Todos los anteriores")
    return input("Seleccione: ")

def generar_liquidacion():
    print("\n¿Desea generar la liquidación de un solo empleado o de todos?")
    print("1. Individual")
    print("2. Global")
    tipo = input("Seleccione: ")

    opcion_informe = seleccionar_tipo_informe()

    print(Fore.CYAN + "\nResumen de selección de informe:")
    print(f"Tipo de informe: {'Individual' if tipo == '1' else 'Global'}")
    print("Contenido del informe:", end=" ")

    if opcion_informe == "1":
        print("Histograma")
    elif opcion_informe == "2":
        print("Pastel")
    elif opcion_informe == "3":
        print("Líneas")
    elif opcion_informe == "4":
        print("PDF con tabla")
    elif opcion_informe == "5":
        print("Todos los anteriores")
    else:
        print(Fore.RED + "Opción inválida." + Style.RESET_ALL)
        return
    print(Style.RESET_ALL)

    if tipo == "1":
        codigo = input("Código del empleado: ")
        empleado = obtener_empleado(codigo)
        if not empleado:
            print(Fore.RED + "Empleado no encontrado." + Style.RESET_ALL)
            return

        salario_base = calcular_salario_basico(empleado["salario"], empleado["dias"])
        auxilio = calcular_auxilio_transporte(empleado["salario"], empleado["dias"])
        deducciones = calcular_deducciones(salario_base)
        total = calcular_total_pago(salario_base, auxilio, deducciones)

        datos = {
            "Salario Básico": salario_base,
            "Auxilio Transporte": auxilio,
            "Deducciones": deducciones,
            "Total a Pagar": total
        }

        imprimir_tabla_empleado(codigo, empleado, datos)

        if opcion_informe in ["1", "2", "3", "5"]:
            tipo_grafico = {
                "1": "barras",
                "2": "pastel",
                "3": "lineas",
                "5": "todos"
            }.get(opcion_informe, "barras")
            generar_graficos(datos, empleado["nombre"], tipo_grafico)

        if opcion_informe in ["4", "5"]:
            generar_pdf_empleado(empleado["nombre"], datos)

        print(Fore.GREEN + "Informe individual generado en la carpeta 'reportes/'." + Style.RESET_ALL)

    elif tipo == "2":
        empleados = listar_empleados()
        imprimir_tabla_global(empleados, calcular_salario_basico, calcular_auxilio_transporte, calcular_deducciones, calcular_total_pago)

        if opcion_informe in ["4", "5"]:
            generar_pdf_global(
                empleados,
                calcular_salario_basico,
                calcular_auxilio_transporte,
                calcular_deducciones,
                calcular_total_pago
            )
            print(Fore.GREEN + "Informe global generado en la carpeta 'reportes/'." + Style.RESET_ALL)

        if opcion_informe in ["1", "2", "3", "5"]:
            tipo_grafico = {
                "1": "barras",
                "2": "pastel",
                "3": "lineas",
                "5": "todos"
            }.get(opcion_informe, "barras")

            for datos in empleados.values():
                salario_base = calcular_salario_basico(datos["salario"], datos["dias"])
                auxilio = calcular_auxilio_transporte(datos["salario"], datos["dias"])
                deducciones = calcular_deducciones(salario_base)
                total = calcular_total_pago(salario_base, auxilio, deducciones)
                info = {
                    "Salario Básico": salario_base,
                    "Auxilio Transporte": auxilio,
                    "Deducciones": deducciones,
                    "Total a Pagar": total
                }
                generar_graficos(info, datos["nombre"], tipo_grafico)

    else:
        print(Fore.RED + "Opción inválida." + Style.RESET_ALL)

def menu_principal():
    while True:
        print(Fore.YELLOW + "\n=== MENÚ PRINCIPAL ===" + Style.RESET_ALL)
        print("1. Registrar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Generar liquidación")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            mostrar_empleados()
        elif opcion == "3":
            actualizar_info_empleado()
        elif opcion == "4":
            generar_liquidacion()
        elif opcion == "5":
            print(Fore.BLUE + "Gracias por usar el sistema de nómina." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opción inválida." + Style.RESET_ALL)
