
from libreria_nomina.constantes import SALARIO_MINIMO, DIAS_LABORALES_MES

def validar_salario(salario):
    return salario >= SALARIO_MINIMO

def validar_dias(dias):
    return 0 < dias <= DIAS_LABORALES_MES

def validar_salario_para_aux_transporte(salario):
    return salario <= (2 * SALARIO_MINIMO)
