# calculos.py

from constantes import SALARIO_MINIMO, AUXILIO_TRANSPORTE, DIAS_LABORALES_MES
from validaciones import validar_salario_para_aux_transporte

def calcular_salario_basico(salario_mensual, dias_trabajados):
    return (salario_mensual / DIAS_LABORALES_MES) * dias_trabajados

def calcular_auxilio_transporte(salario_mensual, dias_trabajados):
    if validar_salario_para_aux_transporte(salario_mensual):
        return (AUXILIO_TRANSPORTE / DIAS_LABORALES_MES) * dias_trabajados
    return 0

def calcular_deduccion_salud(salario_base):
    return salario_base * 0.04

def calcular_deduccion_pension(salario_base):
    return salario_base * 0.04

def calcular_deducciones_totales(salario_base):
    return calcular_deduccion_salud(salario_base) + calcular_deduccion_pension(salario_base)

def calcular_salario_bruto(salario_base, auxilio_transporte):
    return salario_base + auxilio_transporte

def calcular_salario_neto(salario_bruto, deducciones_totales):
    return salario_bruto - deducciones_totales

def calcular_totales_nomina(empleados):
    total_salud = 0
    total_pension = 0
    total_auxilio_transporte = 0
    total_salario_bruto = 0
    total_salario_neto = 0

    for codigo, datos in empleados.items():
        salario_base = calcular_salario_basico(datos["salario"], datos["dias"])
        auxilio = calcular_auxilio_transporte(datos["salario"], datos["dias"])
        salud = calcular_deduccion_salud(salario_base)
        pension = calcular_deduccion_pension(salario_base)
        bruto = calcular_salario_bruto(salario_base, auxilio)
        neto = calcular_salario_neto(bruto, calcular_deducciones_totales(salario_base)) # Recalculamos las totales aquí

        total_salud += salud
        total_pension += pension
        total_auxilio_transporte += auxilio
        total_salario_bruto += bruto
        total_salario_neto += neto

    return {
        "total_salud": total_salud,
        "total_pension": total_pension,
        "total_auxilio_transporte": total_auxilio_transporte,
        "total_salario_bruto": total_salario_bruto,
        "total_salario_neto": total_salario_neto
    }