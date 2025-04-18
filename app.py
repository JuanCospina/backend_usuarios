from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configurar la conexión con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Abrir el documento
sheet = client.open("usuarios_app").sheet1  # o el nombre de tu hoja

# Ruta para agregar un usuario
@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    password = data.get("password")
    sheet.append_row([nombre, correo, password])
    return jsonify({"mensaje": "Usuario agregado con éxito"}), 200

# Ruta para buscar un usuario
@app.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
    data = request.get_json()
    correo_buscado = data.get('correo')
    registros = sheet.get_all_records()

    for registro in registros:
        if registro.get("correo") == correo_buscado:
            return jsonify({"usuario": registro})

    return jsonify({"error": "Usuario no encontrado"}), 404

# Iniciar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
