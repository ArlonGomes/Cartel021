from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'farm.db'

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso (
            nome TEXT PRIMARY KEY,
            dados TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return '🚀 API Controle de Farm online com SQLite!'

@app.route('/salvar', methods=['POST'])
def salvar():
    payload = request.get_json()
    nome = payload.get('nome')
    progresso = payload.get('progresso')
    if not nome or not isinstance(progresso, list):
        return jsonify({'erro': 'Dados inválidos'}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO progresso (nome, dados) VALUES (?, ?)", (nome, str(progresso)))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': f'Dados de {nome} salvos com sucesso!'})

@app.route('/listar', methods=['GET'])
def listar():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, dados FROM progresso")
    rows = cursor.fetchall()
    conn.close()
    dados = {nome: eval(valores) for nome, valores in rows}
    return jsonify(dados)

@app.route('/usuario/<nome>', methods=['GET'])
def obter_usuario(nome):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT dados FROM progresso WHERE nome = ?", (nome,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({nome: eval(row[0])})
    else:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

@app.route('/remover/<nome>', methods=['DELETE'])
def remover(nome):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM progresso WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': f'{nome} removido com sucesso'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
