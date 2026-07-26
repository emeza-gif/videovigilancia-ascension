from flask import Flask, render_template, send_file
import os

app = Flask(__name__)
app.secret_key = 'ascension_seguridad_secreto'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONTACTOS_FOLDER = os.path.join(BASE_DIR, 'contactos')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar-contacto')
def descargar_contacto():
    try:
        archivo_vcf = 'central.vcf'
        ruta_completa = os.path.join(CONTACTOS_FOLDER, archivo_vcf)
        
        if os.path.exists(ruta_completa):
            return send_file(ruta_completa, as_attachment=True, download_name='Central_Seguridad_Ascension.vcf')
        else:
            return "Error: El archivo de contacto no está disponible en el servidor.", 404
    except Exception as e:
        print(f"Error en descarga: {e}")
        return "Ocurrió un error interno al procesar la descarga.", 500

if __name__ == '__main__':
    app.run(debug=True)