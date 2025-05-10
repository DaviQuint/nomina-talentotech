from colorama import Fore, Style

# Imprimir la tabla de liquidación de un empleado
def imprimir_tabla_empleado(codigo, datos_empleado, datos_liquidacion=None):
    print(Fore.CYAN + f"\nLiquidación del empleado {codigo:<5} - {datos_empleado['nombre']:<20}" + Style.RESET_ALL)
    print(f"{'Salario:':<15}${datos_empleado['salario']:<12,.2f} | {'Días trabajados:':<18}{datos_empleado['dias']}" + Style.RESET_ALL)
    if 'direccion' in datos_empleado:
        print(f"{'Dirección:':<15}{datos_empleado['direccion']}")
    if 'correo' in datos_empleado:
        print(f"{'Correo:':<15}{datos_empleado['correo']}")

    if datos_liquidacion:
        print("\n" + Fore.YELLOW + "-" * 50)
        print(f"{'Concepto':<25}{'Valor ($)':>20}")
        print("-" * 50 + Style.RESET_ALL)
        for k, v in datos_liquidacion.items():
            print(f"{k:<25}${v:>20,.2f}")
        print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)

# NUEVA función para imprimir tabla global de empleados
def imprimir_tabla_global(empleados, calcular_salario_basico, calcular_auxilio_transporte, calcular_deduccion_salud, calcular_deduccion_pension, calcular_deducciones_totales, calcular_salario_bruto, calcular_salario_neto):
    if not empleados:
        print(Fore.RED + "\nNo hay empleados registrados." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "\n=== LIQUIDACIÓN GLOBAL DE EMPLEADOS ===" + Style.RESET_ALL)
    encabezados = f"{'Código':<8}{'Nombre':<20}{'Salario':<12}{'Días':<6}{'Básico':<12}{'Auxilio':<12}{'Salud':<10}{'Pensión':<10}{'Deducc.':<12}{'Bruto':<12}{'Neto':<12}{'Dirección':<30}{'Correo':<25}"
    print(Fore.YELLOW + encabezados + Style.RESET_ALL)
    print("-" * len(encabezados))

    for codigo, datos in empleados.items():
        salario = datos["salario"]
        dias = datos["dias"]
        basico = calcular_salario_basico(salario, dias)
        aux = calcular_auxilio_transporte(salario, dias)
        salud = calcular_deduccion_salud(basico)
        pension = calcular_deduccion_pension(basico)
        deduc_totales = calcular_deducciones_totales(basico)
        bruto = calcular_salario_bruto(basico, aux)
        neto = calcular_salario_neto(bruto, deduc_totales)
        direccion = datos.get('direccion', '')
        correo = datos.get('correo', '')

        print(f"{codigo:<8}{datos['nombre']:<20}${salario:<11,.0f}{dias:<6}{basico:<12,.0f}{aux:<12,.0f}{salud:<10,.0f}{pension:<10,.0f}{deduc_totales:<12,.0f}{bruto:<12,.0f}{neto:<12,.0f}{direccion:<30}{correo:<25}")