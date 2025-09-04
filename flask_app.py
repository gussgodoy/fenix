import os
import mysql.connector
from flask import Flask, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados a partir das variáveis de ambiente
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        # Em um app real, você faria um log desse erro
        print(f"Erro de conexão com o banco de dados: {err}")
        return None

@app.route('/')
def home():
    return "API no ar. Acesse /test_db para verificar a conexão com o banco de dados."

@app.route('/test_db')
def test_db_connection():
    """Rota para testar a conexão com o banco de dados."""
    conn = get_db_connection()
    if conn and conn.is_connected():
        conn.close()
        return jsonify({"status": "success", "message": "Conexão com o banco de dados bem-sucedida!"})
    else:
        return jsonify({"status": "error", "message": "Falha ao conectar com o banco de dados."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))