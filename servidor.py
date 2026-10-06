import sqlite3
from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "tareas.db"

def init_db():
    """Crea la base de datos y la tabla de usuarios si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 1. Endpoint: Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"mensaje": "Faltan datos ('usuario' y 'contraseña')"}), 400

    usuario = datos['usuario'].strip()
    contrasena = datos['contraseña']

    if not usuario or not contrasena:
        return jsonify({"mensaje": "Usuario y contraseña no pueden estar vacíos"}), 400

    # Hasheo seguro de contraseña
    contrasena_hash = generate_password_hash(contrasena)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena_hash))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"mensaje": f"Error interno: {str(e)}"}), 500

# 2. Endpoint: Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"mensaje": "Faltan credenciales"}), 400

    usuario = datos['usuario'].strip()
    contrasena = datos['contraseña']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    # Verificación segura del hash
    if resultado and check_password_hash(resultado[0], contrasena):
        return jsonify({"mensaje": "Inicio de sesión exitoso", "acceso": True}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas", "acceso": False}), 401

# 3. Endpoint: Gestión de Tareas (HTML de bienvenida)
@app.route('/tareas', methods=['GET'])
def tareas():
    html_bienvenida = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Gestión de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
            h1 { color: #2c3e50; }
            p { color: #555; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido al Gestor de Tareas!</h1>
            <p>Has accedido correctamente a la API de tareas.</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_bienvenida)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)