
from flask import Flask, render_template, request, send_file
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime
import os

app = Flask(__name__)

EXCEL_PATH = 'trabajadores.xlsx'
TEMPLATE_HTML = 'templates/contrato_template.html'
OUTPUT_DIR = 'output'

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_excel(EXCEL_PATH)
    nombres = df['nombre'].tolist()

    if request.method == "POST":
        nombre_seleccionado = request.form['trabajador']
        trabajador = df[df['nombre'] == nombre_seleccionado].iloc[0].to_dict()

        data = {
            "FECHA_CONTRATO": datetime.today().strftime("%d de %B de %Y"),
            "NOMBRE_COMPLETO": trabajador["nombre"],
            "RUT": trabajador["rut"],
            "FECHA_NACIMIENTO": trabajador["nacimiento"],
            "DIRECCION": trabajador["direccion"],
            "CARGO": trabajador["cargo"],
            "OBRA": trabajador["obra"],
            "DIRECCION_OBRA": trabajador["direccion_obra"],
            "SUELDO_BASE": trabajador["sueldo"],
            "COLACION": trabajador["colacion"],
            "MOVILIZACION": trabajador["movilizacion"],
            "FECHA_INGRESO": trabajador["fecha_inicio"],
            "FECHA_TERMINO": trabajador["fecha_termino"]
        }

        with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
            template = Template(f.read())
            rendered_html = template.render(**data)

        output_pdf_path = os.path.join(OUTPUT_DIR, "contrato_generado.pdf")
        HTML(string=rendered_html).write_pdf(output_pdf_path)

        return send_file(output_pdf_path, as_attachment=True)

    return render_template("formulario.html", nombres=nombres)

if __name__ == "__main__":
    app.run(debug=True)
