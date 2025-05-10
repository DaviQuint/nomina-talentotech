import re
from constantes import SALARIO_MINIMO, DIAS_LABORALES_MES

def validar_salario(salario):
    LIMITE_SALARIO_MAXIMO = 8000000
    return SALARIO_MINIMO <= salario <= LIMITE_SALARIO_MAXIMO

def validar_dias(dias):
    return 0 < dias <= DIAS_LABORALES_MES

def validar_salario_para_aux_transporte(salario):
    return salario <= (2 * SALARIO_MINIMO)

def validar_correo(correo):
    if not correo:
        return True
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, correo) is not None

def validar_direccion(direccion):
    return len(direccion.strip()) > 0

def validar_nombre(nombre):
    if not nombre.strip():
        return False
    patron = r"^[a-zA-Z\s]+$"  # Permite letras y espacios
    return re.match(patron, nombre) is not None