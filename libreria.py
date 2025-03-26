import os #Para limpiar pantalla
import constantes #para llamar constantes
from tabulate import tabulate #para la presentacion
from colorama import Fore, Style, init 

init(autoreset=True)

#Funcion para limpiar pantalla en este caso devuelve el nombre del sistema operativo y aplica el comando respectivo
def limpiarPantalla ():
    if os.name == 'nt':  # Para sistemas Windows
        os.system('cls')
    else:  # Para sistemas Unix/Linux/Mac
        os.system('clear')

#Crear una funcion que muestra datos en pantalla
def mostrar_en_consola(): #Aqui van todos los elementos que se mostraran en la pantalla
    limpiarPantalla() # se comienza limpiando la pantalla de todo lo anterior
    empleados = [] # se abre una lista que contendra los datos personales de los empleados
    i = 1 # esta variable esta hecha para que al usar la funcion "insertar_datos(i)" se ingresen en otra casilla diferente a la anterior, porque esta en un ciclo
    while True: #ciclo para ingresar varios datos sin pausas
        empleado = ingresar_datos(i)
        if empleado is None:
            break # deja de insertar datos si se escribe "salir", esta es la segunda parte

        empleados.append(empleado) #añadir los datos pedidos a la lista
        i += 1

    tabla_datos = [] #Aqui iran las sumas y totales necesarios para mostrar en la pantalla mas abajo de la tabla
    suma_aux_transporte = 0
    suma_salud = 0
    suma_pension = 0
    nomina_total = 0

    for empleado in empleados: #bucle para obtener los calculos de las formulas por cada empleado
        salario_neto_empleado, salario_devengado_total, costos_salud, costos_pension = salario_neto(empleado)

        empleado["salario_neto"] = salario_neto_empleado
        empleado["salario_devengado"] = salario_devengado_total
        empleado["costos_salud"] = costos_salud
        empleado["costos_pension"] = costos_pension

        suma_aux_transporte += empleado['aux_transporte']
        suma_salud += costos_salud
        suma_pension += costos_pension
        nomina_total += salario_neto_empleado + costos_salud + costos_pension

        tabla_datos.append([empleado['ID'], empleado['nombre'], salario_devengado_total, empleado['aux_transporte'], costos_salud + costos_pension, salario_neto_empleado])
    #Aqui acaba el bucle, se calcularon los datos de todos los empleados

    tabla = tabulate(tabla_datos, headers=[Fore.CYAN + "ID" + Style.RESET_ALL, Fore.CYAN + "Nombre" + Style.RESET_ALL, Fore.CYAN + "Sal. Devengado" + Style.RESET_ALL, Fore.CYAN + "Aux de Transporte" + Style.RESET_ALL, Fore.CYAN + "Descuentos" + Style.RESET_ALL, Fore.CYAN + "Sal. Neto" + Style.RESET_ALL], tablefmt="grid") #funcion que, usando tabulate, permite añadir los encabezados a la tabla. tambien incluye la funcion colorama para dar color a los encabezados

    print(tabla) #muestra la tabla
    print(Fore.RED + "Total Subsidio de Transporte:\t" + Style.RESET_ALL, f"{suma_aux_transporte}")
    print(Fore.RED + "Total Costos de Salud:\t\t" + Style.RESET_ALL, f"{suma_salud}")
    print(Fore.RED + "Total Costos de Pensión:\t" + Style.RESET_ALL, f"{suma_pension}")
    print(Fore.RED + "Total Nómina Pagada:\t\t" + Style.RESET_ALL, f"{nomina_total}")
    #Contiene los totales y las palabras en rojo usando colorama

#El print debe tener: Nombre, devengado, aux transporte, descuentos, salario neto, total pagado por subsidio de transporte, total descontado para pension, total descontado para salud, total de la nomina pagada.

#Funcion que ingresa los datos del programa en forma de diccionario:
def ingresar_datos(i):
    datos = {}
    #diccionario vacio, este diccionario se uso durante los procesos pero se decidio crear una lista aparte para procesar los datos al final.
    datos["ID"] = i #el numero del dato actual sigue a i en el ciclo

    # Para validar que se ingresa texto en nombre
    try: 
        nombre = str(input(f"Nombre del empleado {i} (o 'salir'):\n")) #ingrese nombre
        if nombre.lower() == "salir": #si nombre es salir entonces cierre la funcion
            limpiarPantalla()
            return None #Esta funcion conecta con la que mencione anteriormente y es la parte 1, ayuda a que al ingresar "salir" el programa termine de pedir datos
        datos["nombre"] = nombre  # Llamando solo la posicion "nombre" en el diccionario
    except:
        print("Error: Ingrese un nombre válido.")

    while True: #Ciclo que valida si el salario basico mensual esta en el intervalo valido que es entre el salario minimo y 8.000.000
        try: # valida que el salario es int
            datos["salario_basico_mensual"] = int(input(f"Salario Basico Mensual del empleado {i}:\n"))
            if not (constantes.SALARIO_MINIMO <= datos["salario_basico_mensual"] <= 8000000):
            # validacion del intervalo antes mencionado
                print(f"Salario Basico del empleado invalido\n({constantes.SALARIO_MINIMO} - 8000000)")
                continue
            break
        except ValueError:
            print("Error: Ingrese un número válido.")

    while True: #ciclo para validar que se ingresan dias entre 0 y 30
        try:
            datos["dias_trabajados_mes"] = int(input(f"Dias Trabajados en el mes del empleado {i}:\n"))
            if not (0 <= datos["dias_trabajados_mes"] <= 30):
                print(f"Cantidad de dias trabajados del empleado invalidos\n(0 - 30)")
                continue
            break
        except ValueError:
            print("Error: Ingrese un número válido.")

    datos["aux_transporte"] = aux_transporte_valido(datos["salario_basico_mensual"], datos["dias_trabajados_mes"]) #se guardan los datos del auxilio de transporte desde otra funcion. Se hace aqui para que al pasar por cada empleado guarde este valor de una sola vez

    return datos #siempre regresa la tabla que contiene los datos de esta funcion

#Funcion para calcular el salario devengado
def salario_devengado(datos):
    salario_basico_mensual= datos["salario_basico_mensual"] #se obtiene el salario basico mensual de otra funcion
    salario_diario = salario_basico_mensual / 30 #se obtiene el salario basico usando datos anteriores
    dias_trabajados_mes = datos["dias_trabajados_mes"] #se llama este dato desde la tabla que se ingreso como variable arriba
    salario_devengado = salario_diario * dias_trabajados_mes #Se calcula el salario que obtiene el trabajador segun los dias que trabajo y lo que recibiria normalmente
    return salario_devengado, dias_trabajados_mes #se retornan el salario devengado y los dias trabajados

#funcion que valida si obtiene auxilio de transporte
def aux_transporte_valido(salario_basico, dias_trabajados_mes):
    dos_salarios_minimos = constantes.SALARIO_MINIMO * 2
    
    if salario_basico < dos_salarios_minimos:
        aux_transporte = int((constantes.AUX_TRANSPORTE/30) * dias_trabajados_mes)
        return aux_transporte #si lo obtiene, hace los calculos y lo retorna
    else:
        return 0 #no lo obtiene, regresa 0

def salario_neto(datos): #aqui se obtiene el salario neto
    salario_devengado_base, _ = salario_devengado(datos) #se llama el salario devengado desde la funcion "salario devengado(lista)"
    costos_salud = round(salario_devengado_base * constantes.SALUD) #los costos de salud por aparte para llamarlos individualmente mas tarde
    costos_pension = round(salario_devengado_base * constantes.PENSION) #tambien los datos de pension estan por aparte. ambos se obtienen multiplicando el porcentaje dado por el gobierno (4%) y el salario devengado
    salario_devengado_total = int(salario_devengado_base + datos["aux_transporte"]) #Esta variable contiene la suma de salario devengado y auxilio de transporte
    salario_neto = int(salario_devengado_total - costos_salud - costos_pension) #finalmente, el salario neto
    return salario_neto, salario_devengado_total, costos_salud, costos_pension #devuelve varios datos que se usaran mas tarde.
    #Lo que devuelve es: salario neto, salario+auxilio, costos de salud y costos de pension