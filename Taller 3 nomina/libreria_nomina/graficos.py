import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

from libreria_nomina.constantes import CARPETA_REPORTES

# Asegurar que la carpeta reportes exista
os.makedirs(CARPETA_REPORTES, exist_ok=True)

# Crear gráficos
def generar_graficos(datos, nombre_empleado, tipo="todos"):
    conceptos = list(datos.keys())
    valores = list(datos.values())

    if tipo in ["barras", "todos"]:
        plt.figure(figsize=(6, 4))
        plt.bar(conceptos, valores, color='skyblue')
        plt.title(f'Liquidación de {nombre_empleado} - Barras')
        plt.ylabel("Valor $")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{CARPETA_REPORTES}/{nombre_empleado}_barras.png")
        plt.close()

    if tipo in ["pastel", "todos"]:
        plt.figure(figsize=(5, 5))
        plt.pie(valores, labels=conceptos, autopct='%1.1f%%', startangle=90)
        plt.title(f'Liquidación de {nombre_empleado} - Pastel')
        plt.tight_layout()
        plt.savefig(f"{CARPETA_REPORTES}/{nombre_empleado}_pastel.png")
        plt.close()

    if tipo in ["lineas", "todos"]:
        plt.figure(figsize=(6, 4))
        plt.plot(conceptos, valores, marker='o', color='green')
        plt.title(f'Liquidación de {nombre_empleado} - Líneas')
        plt.ylabel("Valor $")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{CARPETA_REPORTES}/{nombre_empleado}_lineas.png")
        plt.close()

# PDF de un empleado
def generar_pdf_empleado(nombre_empleado, datos_liquidacion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Informe de Liquidación - {nombre_empleado}", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 10, "Concepto", 1)
    pdf.cell(50, 10, "Valor ($)", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 12)
    for concepto, valor in datos_liquidacion.items():
        pdf.cell(90, 10, concepto, 1)
        pdf.cell(50, 10, f"${valor:,.2f}", 1)
        pdf.ln()

    ruta = f"{CARPETA_REPORTES}/{nombre_empleado}_liquidacion.pdf"
    pdf.output(ruta)

# PDF global con todos los empleados
def generar_pdf_global(empleados, calcular_salario_basico, calcular_auxilio_transporte, calcular_deducciones, calcular_total_pago):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Informe Global de Liquidaciones", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)

    # Encabezados de tabla
    pdf.set_font("Arial", "B", 10)
    headers = ["Código", "Nombre", "Salario", "Días", "Básico", "Auxilio", "Deducciones", "Total"]
    widths = [20, 30, 25, 15, 25, 25, 30, 25]

    for i, header in enumerate(headers):
        pdf.cell(widths[i], 10, header, 1)
    pdf.ln()

    # Datos por empleado
    pdf.set_font("Arial", "", 9)
    for codigo, datos in empleados.items():
        salario = datos["salario"]
        dias = datos["dias"]
        basico = calcular_salario_basico(salario, dias)
        aux = calcular_auxilio_transporte(salario, dias)
        deduc = calcular_deducciones(basico)
        total = calcular_total_pago(basico, aux, deduc)

        fila = [codigo, datos["nombre"], f"${salario:,.0f}", str(dias),
                f"${basico:,.0f}", f"${aux:,.0f}", f"${deduc:,.0f}", f"${total:,.0f}"]
        
        for i, valor in enumerate(fila):
            pdf.cell(widths[i], 10, valor, 1)
        pdf.ln()

    ruta = f"{CARPETA_REPORTES}/informe_global_liquidaciones.pdf"
    pdf.output(ruta)
