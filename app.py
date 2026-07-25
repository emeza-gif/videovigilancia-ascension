from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Asegurar que la carpeta database exista
os.makedirs('database', exist_ok=True)
DB_NAME = 'database/database.db'

def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS encuestas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT,
                nombres TEXT,
                atencion TEXT,
                turno TEXT,
                solicitud TEXT,
                informacion TEXT,
                trato INTEGER,
                rapidez TEXT,
                comentarios TEXT,
                operador TEXT
            )
        """)
        con.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encuesta')
def encuesta():
    return render_template('encuesta.html')

# Se actualizó la ruta a '/guardar-encuesta' para que coincida exactamente con tu HTML
@app.route('/guardar-encuesta', methods=['POST'])
def guardar():
    dni = request.form.get('dni')
    nombres = request.form.get('nombres')
    
    atencion = request.form.get('atencion')
    turno = request.form.get('turno')
    solicitudes = request.form.getlist('solicitud') # Usar getlist para checkboxes múltiples
    solicitud_str = ', '.join(solicitudes) if isinstance(solicitudes, list) else (solicitudes or '')
    informacion = request.form.get('informacion')
    trato = request.form.get('trato')
    rapidez = request.form.get('rapidez')
    comentarios = request.form.get('comentarios')
    operador = request.form.get('operador', 'Operador Turno General')

    with conectar() as con:
        con.execute("""
            INSERT INTO encuestas (dni, nombres, atencion, turno, solicitud, informacion, trato, rapidez, comentarios, operador)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dni, nombres, atencion, turno, solicitud_str, informacion, trato, rapidez, comentarios, operador))
        con.commit()

    return redirect(url_for('gracias'))

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/dashboard')
def dashboard():
    with conectar() as con:
        # Total de encuestas
        total_encuestas = con.execute("SELECT COUNT(*) FROM encuestas").fetchone()[0]
        
        # Promedio general de trato (escala 1 a 5)
        promedio = con.execute("SELECT AVG(trato) FROM encuestas").fetchone()[0]
        promedio = round(promedio, 1) if promedio else 0

        # Datos para gráfico de calificaciones
        cursor = con.execute("SELECT atencion, COUNT(*) FROM encuestas GROUP BY atencion")
        resultados = cursor.fetchall()
        labels = [fila[0] for fila in resultados]
        valores = [fila[1] for fila in resultados]

        # Lista detallada de todas las respuestas para tu tabla en el panel
        cursor_detalles = con.execute("SELECT id, atencion, trato, comentarios FROM encuestas ORDER BY id DESC")
        registros = cursor_detalles.fetchall()

    return render_template('panel.html', 
                           total_encuestas=total_encuestas, 
                           promedio=promedio, 
                           labels=labels, 
                           valores=valores,
                           registros=registros)

@app.route('/panel')
def panel():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
