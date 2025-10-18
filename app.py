import os
import psycopg2
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def get_db_connection():
    """Establece conexión a la base de datos PostgreSQL usando variables de entorno."""
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'mensajesdb'),
            user=os.getenv('DB_USER', 'admin'),
            password=os.getenv('DB_PASSWORD', 'admin123')
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def init_database():
    """Inicializa la tabla mensajes si no existe."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mensajes (
                    id SERIAL PRIMARY KEY,
                    texto VARCHAR(100)
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"Error al crear la tabla: {e}")
            return False
    return False

@app.route('/', methods=['GET'])
def index():
    """Endpoint raíz que confirma conexión a la base de datos."""
    conn = get_db_connection()
    if conn:
        try:
            # Inicializar la tabla si es necesario
            init_database()
            conn.close()
            return "App connected to PostgreSQL", 200
        except Exception as e:
            return f"Error de conexión: {str(e)}", 500
    else:
        return "Error: No se pudo conectar a PostgreSQL", 500

@app.route('/add', methods=['POST'])
def add_message():
    """Añade un nuevo mensaje a la base de datos."""
    # Obtener el texto del parámetro query o usar valor por defecto
    texto = request.args.get('texto', 'Sin mensaje')
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mensajes (texto) VALUES (%s)",
                (texto,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return f"Message added: {texto}", 201
        except psycopg2.Error as e:
            return f"Error al insertar mensaje: {str(e)}", 500
    else:
        return "Error: No se pudo conectar a PostgreSQL", 500

@app.route('/list', methods=['GET'])
def list_messages():
    """Devuelve todos los mensajes almacenados."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, texto FROM mensajes ORDER BY id")
            rows = cursor.fetchall()
            
            # Convertir las filas a formato JSON
            mensajes = []
            for row in rows:
                mensajes.append({
                    'id': row[0],
                    'texto': row[1]
                })
            
            cursor.close()
            conn.close()
            return jsonify({"mensajes": mensajes}), 200
        except psycopg2.Error as e:
            return f"Error al obtener mensajes: {str(e)}", 500
    else:
        return "Error: No se pudo conectar a PostgreSQL", 500

if __name__ == '__main__':
    # Inicializar la base de datos al arrancar
    print("Inicializando aplicación Flask...")
    if init_database():
        print("Base de datos inicializada correctamente")
    else:
        print("Advertencia: No se pudo inicializar la base de datos")
    
    # Ejecutar la aplicación en todas las interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)