CREATE TABLE IF NOT EXISTS encuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atencion TEXT NOT NULL,
    turno TEXT NOT NULL,
    solicitud TEXT NOT NULL,
    informacion TEXT NOT NULL,
    trato INTEGER NOT NULL,
    rapidez TEXT NOT NULL,
    comentarios TEXT,
    operador TEXT DEFAULT 'Desconocido',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);