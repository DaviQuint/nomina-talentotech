from colorama import Fore, Style

# Imprimir la tabla de liquidación de un empleado
def imprimir_tabla_empleado(codigo, datos_empleado, datos_liquidacion=None):
    print(Fore.CYAN + f"\nLiquidación del empleado {codigo} - {datos_empleado['nombre']}" + Style.RESET_ALL)
    print(f"Salario: ${datos_empleado['salario']:,.2f} | Días trabajados: {datos_empleado['dias']}")
    
    if datos_liquidacion:
        print("\n" + Fore.YELLOW + "-" * 40)
        print(f"{'Concepto':<25}{'Valor ($)':>12}")
        print("-" * 40 + Style.RESET_ALL)
        for k, v in datos_liquidacion.items():
            print(f"{k:<25}${v:>12,.2f}")
        print(Fore.YELLOW + "-" * 40 + Style.RESET_ALL)

# NUEVA función para imprimir tabla global de empleados
def imprimir_tabla_global(empleados, calcular_salario_basico, calcular_auxilio_transporte, calcular_deducciones, calcular_total_pago):
    if not empleados:
        print(Fore.RED + "\nNo hay empleados registrados." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "\n=== LIQUIDACIÓN GLOBAL DE EMPLEADOS ===" + Style.RESET_ALL)
    encabezados = f"{'Código':<10}{'Nombre':<15}{'Salario':<12}{'Días':<6}{'Básico':<12}{'Auxilio':<12}{'Deducciones':<14}{'Total':<12}"
    print(Fore.YELLOW + encabezados + Style.RESET_ALL)
    print("-" * len(encabezados))

    for codigo, datos in empleados.items():
        salario = datos["salario"]
        dias = datos["dias"]
        basico = calcular_salario_basico(salario, dias)
        aux = calcular_auxilio_transporte(salario, dias)
        deduc = calcular_deducciones(basico)
        total = calcular_total_pago(basico, aux, deduc)

        print(f"{codigo:<10}{datos['nombre']:<15}${salario:<11,.0f}{dias:<6}{basico:<12,.0f}{aux:<12,.0f}{deduc:<14,.0f}{total:<12,.0f}")
