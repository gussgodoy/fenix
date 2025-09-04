import os
from flask import Flask
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "API no ar."

if __name__ == '__main__':
    # O Render ignora isso e usa o Gunicorn, mas é útil para testes locais
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))