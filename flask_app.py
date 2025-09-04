import os
import pymysql
from flask import Flask, jsonify
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
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4',
        ssl={'ca': SSL_CERT_PATH}
    )

# 3. ROTA DE TESTE PRINCIPAL
@app.route('/')
def index():
    return "<h1>O servidor Fênix está no ar!</h1>"

# 4. ROTA DE TESTE DE SAÚDE E CONEXÃO COM A DB
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
        if conn:
            conn.close()
    return jsonify({
        "server_status": "OK", 
        "app_version": "Minimal Test", 
        "database_status": db_status
    }), 200

# Ponto de entrada para Gunicorn
if __name__ == '__main__':
    app.run()