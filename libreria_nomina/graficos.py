# graficos.py
import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from colorama import Fore, Style
import calendar
from libreria_nomina.calculos import (
    calcular_salario_basico,
    calcular_auxilio_transporte,
    calcular_deducciones_totales,
    calcular_salario_bruto,
)
from libreria_nomina.constantes import CARPETA_REPORTES

# Asegurar que la carpeta reportes exista
os.makedirs(CARPETA_REPORTES, exist_ok=True)

# Crear gráficos individuales (sin cambios por ahora)
def generar_graficos(datos, nombre_empleado, tipo="todos"):
    conceptos = list(datos.keys())
    valores = list(datos.values())
    rutas_graficos = {}

    if tipo in ["barras", "todos"]:
        plt.figure(figsize=(6, 4))
        plt.bar(conceptos, valores, color='skyblue')
        plt.title(f'Liquidación de {nombre_empleado} - Barras')
        plt.ylabel("Valor $")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        ruta = f"{CARPETA_REPORTES}/{nombre_empleado}_barras.png"
        try:
            plt.savefig(ruta)
            rutas_graficos["barras"] = ruta
        except Exception as e:
            print(Fore.RED + f"Error al guardar gráfico de barras: {e}" + Style.RESET_ALL)
        plt.close()

    if tipo in ["pastel", "todos"]:
        plt.figure(figsize=(5, 5))
        plt.pie(valores, labels=conceptos, autopct='%1.1f%%', startangle=90)
        plt.title(f'Liquidación de {nombre_empleado} - Pastel')
        plt.tight_layout()
        ruta = f"{CARPETA_REPORTES}/{nombre_empleado}_pastel.png"
        try:
            plt.savefig(ruta)
            rutas_graficos["pastel"] = ruta
        except Exception as e:
            print(Fore.RED + f"Error al guardar gráfico de pastel: {e}" + Style.RESET_ALL)
        plt.close()

    if tipo in ["lineas", "todos"]:
        plt.figure(figsize=(6, 4))
        plt.plot(conceptos, valores, marker='o', color='green')
        plt.title(f'Liquidación de {nombre_empleado} - Líneas')
        plt.ylabel("Valor $")
        plt.xticks(rotation=45, ha="right")
        plt.grid(True)
        plt.tight_layout()
        ruta = f"{CARPETA_REPORTES}/{nombre_empleado}_lineas.png"
        try:
            plt.savefig(ruta)
            rutas_graficos["lineas"] = ruta
        except Exception as e:
            print(Fore.RED + f"Error al guardar gráfico de líneas: {e}" + Style.RESET_ALL)
        plt.close()

    return rutas_graficos

def generar_pdf_reporte_empleados(empleados, calcular_salario_basico, calcular_deducciones_totales, calcular_salario_neto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Empleados (Salario, Deducciones, Neto)", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 9)
    headers = ["Código", "Nombre", "Básico", "Deducciones", "Neto", "Estado"]  # Añadir "Estado"
    widths = [15, 40, 30, 30, 30, 15]  # Añadir ancho para "Estado"
    for i, header in enumerate(headers):
        pdf.cell(widths[i], 7, header, 1)
    pdf.ln()
    pdf.set_font("Arial", "", 8)
    for codigo, datos in empleados.items():
        salario_base = calcular_salario_basico(datos['salario'], datos['dias'])
        deducciones = calcular_deducciones_totales(salario_base)
        salario_neto = calcular_salario_neto(calcular_salario_bruto(salario_base, calcular_auxilio_transporte(datos['salario'], datos['dias'])), deducciones)
        fila = [codigo, datos["nombre"], f"${salario_base:,.2f}", f"${deducciones:,.2f}", f"${salario_neto:,.2f}", datos["estado"]]  # Añadir estado
        for i, valor in enumerate(fila):
            pdf.cell(widths[i], 7, valor, 1)
        pdf.ln()
    ruta = f"{CARPETA_REPORTES}/reporte_empleados_detallado.pdf"
    try:
        pdf.output(ruta)
    except Exception as e:
        print(Fore.RED + f"Error al guardar PDF de reporte de empleados: {e}" + Style.RESET_ALL)

# PDF global con todos los empleados (sin cambios por ahora)
def generar_pdf_global(empleados, calcular_salario_basico, calcular_auxilio_transporte, calcular_deduccion_salud, calcular_deduccion_pension, calcular_deducciones_totales, calcular_salario_bruto, calcular_salario_neto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Informe Global de Liquidaciones", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    # Encabezados de tabla
    pdf.set_font("Arial", "B", 9)
    headers = ["Código", "Nombre", "Salario", "Días", "Básico", "Auxilio", "Salud", "Pensión", "Deducc.", "Bruto", "Neto", "Estado"]  # Añadir "Estado"
    widths = [15, 25, 20, 10, 20, 20, 15, 15, 20, 20, 20, 15]  # Añadir ancho para "Estado"
    for i, header in enumerate(headers):
        pdf.cell(widths[i], 7, header, 1)
    pdf.ln()
    # Datos por empleado
    pdf.set_font("Arial", "", 8)
    for codigo, datos in empleados.items():
        salario = datos["salario"]
        dias = datos["dias"]
        basico = calcular_salario_basico(salario, dias)
        aux = calcular_auxilio_transporte(salario, dias)
        salud = calcular_deduccion_salud(basico)
        pension = calcular_deduccion_pension(basico)
        deduc = calcular_deducciones_totales(basico)
        bruto = calcular_salario_bruto(basico, aux)
        neto = calcular_salario_neto(bruto, deduc)
        fila = [codigo, datos["nombre"], f"${salario:,.0f}", str(dias),
                f"${basico:,.0f}", f"${aux:,.0f}", f"${salud:,.0f}", f"${pension:,.0f}",
                f"${deduc:,.0f}", f"${bruto:,.0f}", f"${neto:,.0f}", datos["estado"]]  # Añadir estado
        for i, valor in enumerate(fila):
            pdf.cell(widths[i], 7, valor, 1)
        pdf.ln()
    ruta = f"{CARPETA_REPORTES}/informe_global_liquidaciones.pdf"
    try:
        pdf.output(ruta)
    except Exception as e:
        print(Fore.RED + f"Error al guardar PDF global: {e}" + Style.RESET_ALL)

# Nueva función para generar PDF con gráficos de pagos por mes
def generar_pdf_graficos_pagos_mes(empleados, calcular_salario_neto, anio):
    pagos_por_mes = {i: 0 for i in range(1, 13)}
    for codigo, datos in empleados.items():
        mes_pago = datetime.now().month # **Importante: Esto debe basarse en la fecha real de la nómina**
        salario_base = calcular_salario_basico(datos['salario'], datos['dias'])
        deducciones = calcular_deducciones_totales(salario_base)
        salario_neto = calcular_salario_neto(calcular_salario_bruto(salario_base, calcular_auxilio_transporte(datos['salario'], datos['dias'])), deducciones)
        pagos_por_mes[mes_pago] += salario_neto

    meses_nombres = [calendar.month_name[i] for i in range(1, 13)]
    valores_pagos = list(pagos_por_mes.values())
    rutas_graficos = {}

    # Generar y guardar histograma
    plt.figure(figsize=(10, 6))
    plt.bar(meses_nombres, valores_pagos, color='skyblue')
    plt.xlabel("Mes")
    plt.ylabel("Total Pagado")
    plt.title(f"Total Pagado por Mes - Año {anio} (Histograma)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    ruta_histo = f"{CARPETA_REPORTES}/pagos_mes_histo_{anio}.png"
    try:
        plt.savefig(ruta_histo)
        rutas_graficos["histograma"] = ruta_histo
    except Exception as e:
        print(Fore.RED + f"Error al guardar histograma de pagos por mes: {e}" + Style.RESET_ALL)
    plt.close()

    # Generar y guardar gráfico de pastel
    plt.figure(figsize=(8, 8))
    plt.pie(valores_pagos, labels=meses_nombres, autopct='%1.1f%%', startangle=90)
    plt.title(f"Distribución de Pagos por Mes - Año {anio} (Pastel)")
    plt.tight_layout()
    ruta_pastel = f"{CARPETA_REPORTES}/pagos_mes_pastel_{anio}.png"
    try:
        plt.savefig(ruta_pastel)
        rutas_graficos["pastel"] = ruta_pastel
    except Exception as e:
        print(Fore.RED + f"Error al guardar gráfico de pastel de pagos por mes: {e}" + Style.RESET_ALL)
    plt.close()

    # Generar y guardar gráfico de líneas
    plt.figure(figsize=(10, 6))
    plt.plot(meses_nombres, valores_pagos, marker='o', linestyle='-', color='green')
    plt.xlabel("Mes")
    plt.ylabel("Total Pagado")
    plt.title(f"Tendencia de Pagos por Mes - Año {anio} (Líneas)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    plt.tight_layout()
    ruta_lineas = f"{CARPETA_REPORTES}/pagos_mes_lineas_{anio}.png"
    try:
        plt.savefig(ruta_lineas)
        rutas_graficos["lineas"] = ruta_lineas
    except Exception as e:
        print(Fore.RED + f"Error al guardar gráfico de líneas de pagos por mes: {e}" + Style.RESET_ALL)
    plt.close()

    # Crear PDF con los gráficos
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Gráficos de Pagos por Mes - Año {anio}", ln=True, align="C")
    pdf.ln(10)

    y_pos = 30
    for tipo, ruta in rutas_graficos.items():
        try:
            pdf.image(ruta, x=10, y=y_pos, w=190)
            y_pos += 70  # Ajustar la posición vertical para el siguiente gráfico
            if y_pos > 270: # Nueva página si se alcanza el límite
                pdf.add_page()
                y_pos = 30
        except Exception as e:
            print(Fore.RED + f"Error al insertar gráfico {tipo} en PDF: {e}" + Style.RESET_ALL)

    ruta_pdf = f"{CARPETA_REPORTES}/graficos_pagos_mes_{anio}.pdf"
    try:
        pdf.output(ruta_pdf)
        print(Fore.GREEN + f"Reporte PDF con gráficos de pagos por mes ({anio}) generado en: {ruta_pdf}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error al guardar PDF con gráficos de pagos por mes: {e}" + Style.RESET_ALL)