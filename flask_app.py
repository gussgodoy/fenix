import os
import pymysql
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

# 1. CONFIGURAÇÃO BÁSICA
app = Flask(__name__)
CORS(app)
SSL_CERT_PATH = "ca.pem"

# 2. FUNÇÃO DE CONEXÃO COM O BANCO DE DADOS
def get_db_connection():
    db_host = os.environ.get("DB_HOST")
    db_port = int(os.environ.get("DB_PORT", 3306))
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    return pymysql.connect(
        host=db_host, port=db_port, user=db_user, password=db_password,
        database=db_name, cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4', ssl={'ca': SSL_CERT_PATH}
    )

# 3. ROTAS DE TESTE E SAÚDE
@app.route('/')
def index():
    return "<h1>O servidor Fênix está no ar!</h1>"

@app.route('/api/health', methods=['GET'])
def server_health_check():
    conn = None
    db_status = ""
    try:
        conn = get_db_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    finally:
        if conn: conn.close()
    return jsonify({
        "server_status": "OK", "app_version": "v1.0.2 - Chaves API", "database_status": db_status
    }), 200

# 4. ROTAS PARA GERENCIAMENTO DE CHAVES DE API (CORRIGIDO)

@app.route('/api/chaves', methods=['GET'])
def get_chaves():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, chave, nivel_acesso, ativa, DATE_FORMAT(data_criacao, '%%d/%%m/%%Y %%H:%%i') as data_criacao FROM chaves_api ORDER BY id DESC")
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

@app.route('/api/chaves', methods=['POST'])
def create_chave():
    data = request.get_json()
    nome = data.get('nome')
    if not nome or not nome.strip():
        return jsonify({"status": "error", "message": "O campo 'nome' é obrigatório."}), 400
    nova_chave = f"fenix-{uuid.uuid4()}"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO chaves_api (nome, chave) VALUES (%s, %s)", (nome, nova_chave))
            conn.commit()
            cursor.execute("SELECT id, nome, chave, ativa, DATE_FORMAT(data_criacao, '%%d/%%m/%%Y %%H:%%i') as data_criacao FROM chaves_api WHERE chave = %s", (nova_chave,))
            return jsonify({"status": "success", "data": cursor.fetchone()}), 201
    finally:
        conn.close()

@app.route('/api/chaves/<int:chave_id>', methods=['PUT'])
def update_chave_status(chave_id):
    data = request.get_json()
    if 'ativa' not in data:
        return jsonify({"status": "error", "message": "O campo 'ativa' é obrigatório."}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            rows = cursor.execute("UPDATE chaves_api SET ativa = %s WHERE id = %s", (bool(data['ativa']), chave_id))
            conn.commit()
        return jsonify({"status": "success"}) if rows > 0 else jsonify({"status": "error", "message": "Chave não encontrada."}), 404
    finally:
        conn.close()

@app.route('/api/chaves/<int:chave_id>', methods=['DELETE'])
def delete_chave(chave_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            rows = cursor.execute("DELETE FROM chaves_api WHERE id = %s", (chave_id,))
            conn.commit()
        return jsonify({"status": "success"}) if rows > 0 else jsonify({"status": "error", "message": "Chave não encontrada."}), 404
    finally:
        conn.close()

# Ponto de entrada
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)