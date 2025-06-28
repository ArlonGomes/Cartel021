from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Libera acesso de outros domínios

DATA_FILE = 'dados_farm.json'

# Inicializa o arquivo de dados se não existir
def carregar_dados():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DATA_FILE, 'w') as f:
        json.dump(dados, f, indent=2)

@app.route('/salvar', methods=['POST'])
def salvar():
    payload = request.get_json()
    nome = payload.get('nome')
    progresso = payload.get('progresso')  # Lista de inteiros
    if not nome or not isinstance(progresso, list):
        return jsonify({'erro': 'Dados inválidos'}), 400

    dados = carregar_dados()
    dados[nome] = progresso
    salvar_dados(dados)
    return jsonify({'mensagem': f'Dados de {nome} salvos com sucesso!'})

@app.route('/listar', methods=['GET'])
def listar():
    dados = carregar_dados()
    return jsonify(dados)

@app.route('/usuario/<nome>', methods=['GET'])
def obter_usuario(nome):
    dados = carregar_dados()
    if nome in dados:
        return jsonify({nome: dados[nome]})
    else:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

@app.route('/remover/<nome>', methods=['DELETE'])
def remover(nome):
    dados = carregar_dados()
    if nome in dados:
        del dados[nome]
        salvar_dados(dados)
        return jsonify({'mensagem': f'{nome} removido com sucesso'})
    else:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
