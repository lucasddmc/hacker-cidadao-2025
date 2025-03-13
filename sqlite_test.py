from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Mock database (In-Memory)
gestantes = {
    1: {
        "nome": "Letícia",
        "telefone": "000000000",
        "semana_gestacao": 0, 
        "filhos": []
    }
}  # Stores mothers data
bebes = {}
consultas = {
    1: {
        "tipo": "pre-natal", 
        "data": datetime.datetime.now(), 
        "mother_id": 1
    }
}

mensagens = []  # Stores sent messages (mock for SMS/WhatsApp)

# Generate unique ID (simple counter)
mother_id_counter = 2
baby_id_count = 1


def send_mock_message(mother_id, message, channel="SMS"):
    """ Simulates sending a message via SMS or WhatsApp """
    mensagens.append({
        "mother_id": mother_id,
        "message": message,
        "channel": channel,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    print(f"[{channel} Message] -> {message}")  # Simulate sending


@app.route('/api/mother', methods=['POST'])
def add_mother():
    """ Adds a new mother to the system (mock insert) """
    global mother_id_counter
    data = request.get_json()

    mother_id = mother_id_counter
    mother_id_counter += 1

    gestantes[mother_id] = {
        "nome": data.get("nome"),
        "telefone": data.get("telefone"),
        "semana_gestacao": data.get("semana_gestacao", 0), 
        "filhos": data.get("filhos", [])
    }

    # First welcome message
    send_mock_message(mother_id, f"Olá {data.get('nome')}! Bem-vinda ao programa Mãe Coruja Recife.", "WhatsApp")

    return jsonify({"id": mother_id, "message": "Mãe cadastrada com sucesso!"}), 201


@app.route('/api/mother/<int:mother_id>', methods=['PUT'])
def update_mother(mother_id):
    """ Updates pregnancy week and triggers automatic messages """
    if mother_id not in gestantes:
        return jsonify({"error": "Mãe não encontrada"}), 404

    data = request.get_json()
    new_week = data.get("semana_gestacao")

    if new_week is not None:
        old_week = gestantes[mother_id]["semana_gestacao"]
        gestantes[mother_id]["semana_gestacao"] = new_week

        # Send milestone-based messages
        if old_week < 12 <= new_week:
            send_mock_message(mother_id,
                              "Parabéns! Você completou 3 meses de gravidez. Não se esqueça da consulta pré-natal.",
                              "SMS")
        if old_week < 24 <= new_week:
            send_mock_message(mother_id, "Você atingiu 6 meses de gravidez! Hora de planejar o parto no SUS.",
                              "WhatsApp")

    return jsonify({"message": "Dados atualizados com sucesso!"}), 200


@app.route('/api/messages', methods=['GET'])
def list_messages():
    """ Lists all mock messages sent """
    return jsonify(mensagens)

#no birth precisa ser enviado as informações do bebê 
@app.route('/api/birth', methods=['POST'])
def birth_event():
    """ Simulates a birth event and sends postpartum messages """
    data = request.get_json()
    mother_id = data.get("mae_id")
    nome_bebe = data.get("nome_bebe")

    if mother_id not in gestantes:
        return jsonify({"error": "Mãe não encontrada"}), 404

    global baby_id_counter
    baby_id = baby_id_counter
    baby_id_counter += 1
    bebes[baby_id] = {
        "nome": nome_bebe, 
        "vivo": data.get("vivo"), 
        "nascimento": data.get("nascimento"), 
        "mother_id": mother_id
    }
    # Simulate postpartum message
    if(vivo == True): 
        send_mock_message(mother_id, f"Parabéns pelo nascimento do bebê {nome_bebe}! Agende a consulta pós-parto.", "SMS")
    else: 
        #implementar como lidar com natimortos 

    return jsonify({"message": f"Notificação de nascimento enviada para {gestantes[mother_id]['nome']}"}), 201




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)