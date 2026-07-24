from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
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
@app.route('/guardar', methods=['POST'])

def guardar():
    # Nuevos campos de identificación rápida
    dni = request.form.get('dni')
    nombres = request.form.get('nombres')
    
    # Campos de la encuesta
    atencion = request.form.get('atencion')
    turno = request.form.get('turno')
    solicitudes = request.form.get('solicitud')
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

    return redirect('/gracias')

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

    return render_template('dashboard.html', 
                           total_encuestas=total_encuestas, 
                           promedio=promedio, 
                           labels=labels, 
                           valores=valores)

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
