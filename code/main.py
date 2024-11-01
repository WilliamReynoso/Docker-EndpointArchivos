import os
import psycopg2
from psycopg2 import sql
from flask import Flask, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
UPLOAD_FOLDER = "/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuracion de Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["15 per day", "10 per hour"],  # Límite global (ejemplo: 10 peticiones por hora)
    headers_enabled=os.getenv("RATELIMIT_HEADERS_ENABLED", "true").lower() in ["true", "1"]
)

# Configuracion de la conexion a la base de datos
def get_db_connection():
    connection = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB","none"),
        user=os.getenv("POSTGRES_USER", "none"),
        password=os.getenv("POSTGRES_PASSWORD", "none")
    )
    return connection

@app.route('/')
@limiter.limit("3 per minute")
def home():
    return "Hello world!\nAqui tienes un limite de 3 peticiones por minuto :)"

@app.route('/pagina')
def pagina():
    return "Esta es la página en el endpoint /pagina.\nSin limite especifico pero es Afectado por el limite global de 10 por hora c:"

@app.route('/usuarios')
@limiter.limit("2 per minute")  # Limitar la consulta de usuarios a 2 por min
def usuarios():
    # Funcion para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexion con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexion
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

@app.route('/usuarios/torre')
@limiter.limit("3 per minute")  # Limitar la consulta específica de usuarios a 3 por hora
def usuariostorre():
    # Funcion para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexión con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users WHERE device = 'desktop'")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No se envió ningún archivo"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "Nombre de archivo vacío"}, 400
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            return {"error": "El archivo ya existe"}, 400
        try:
            file.save(file_path)
            return {"message": "Archivo cargado exitosamente"}, 201
        except Exception as e:
            return {"error": f"Error al guardar el archivo: {str(e)}"}, 500
    else:
        return {"error": "Tipo de archivo no permitido"}, 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if allowed_file(filename):
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        except FileNotFoundError:
            return {"error": "Archivo no encontrado"}, 404
    else:
        return {"error": "Tipo de archivo no permitido"}, 400

# Manejo de usuarios bloqueados por exceder el límite
@app.errorhandler(429)
def ratelimit_handler(e):
    return {"error": "Limite de peticiones excedido. Intentelo de nuevo más tarde.  " + str(e)}, 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
