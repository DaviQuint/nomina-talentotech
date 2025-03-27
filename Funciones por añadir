# Constantes
AUX_TRANSPORTE = 200000 #Auxilio de transporte 2025 en Colombia
SALARIO_MINIMO = 1423500 #Salario minimo 2025 en Colombia
SALUD = 0.04 # 4% del salario devengado sin contar auxilio de transporte
PENSION = 0.04


### FUNCIONES ####
#Funcion para calcular el salario devengado
def calcular_salario_devengado(salario_basico, dias_laborados):
    return ((salario_basico/30)*dias_laborados)
    
    
#Funcion para calcular auxilio de transporte 
"""def calcular_auxilio_transporte(salario_basico):
    if salario_basico < (2*SALARIO_MINIMO):
        return 200000 #valor auxilio transporte actual
    else:
        return 0"""

#La funcion esta perfecta, pero el nombre mas correcto seria validacion y no calculo, aunque es solo una opinion, no sé que opinen.
def validar_auxilio_transporte(salario_basico):
    if salario_basico < (2*SALARIO_MINIMO):
        return 200000 #valor auxilio transporte actual
    else:
        return 0

#Funcion para calcular descuentos
def calcular_descuentos(salario_devengado):
    descuento_salud= salario_devengado*SALUD
    descuento_pension=salario_devengado*PENSION
    return descuento_salud, descuento_pension

#Pienso que es mejor hacer los descuentos separados, aunque si lo dejamos así no hay ningún problema.
"""def descuento_salud(salario_devengado):
    return salario_devengado*SALUD
def descuento_pension(salario_devengado):
    return salario_devengado*PENSION"""
    
    
    



