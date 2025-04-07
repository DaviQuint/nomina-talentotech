# calculos.py

from libreria_nomina.constantes import SALARIO_MINIMO, AUXILIO_TRANSPORTE, DIAS_LABORALES_MES
from libreria_nomina.validaciones import validar_salario_para_aux_transporte

def calcular_salario_basico(salario_mensual, dias_trabajados):
    return (salario_mensual / DIAS_LABORALES_MES) * dias_trabajados

def calcular_auxilio_transporte(salario_mensual, dias_trabajados):
    if validar_salario_para_aux_transporte(salario_mensual):
        return (AUXILIO_TRANSPORTE / DIAS_LABORALES_MES) * dias_trabajados
    return 0

def calcular_deducciones(salario_base):
    salud = salario_base * 0.04
    pension = salario_base * 0.04
    return salud + pension

def calcular_total_pago(salario_base, auxilio, deducciones):
    return salario_base + auxilio - deducciones
