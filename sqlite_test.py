from flask import Flask, request, jsonify
from datetime import datetime
from send_message import send_message, send_message_with_buttons, send_message_with_keyboard, handle_updates
import time
import threading


app = Flask(__name__)
# Mock database (In-Memory) with one pre-populated pregnant woman
gestantes = {
    1: {
        "nome": "Ana Souza",
        "telefone": "+5581999999999",
        "inicio_gestacao": "19/12/2024", 
        "primeira_consulta": "13/02/2025"
    }
}

unidades_saude = [
    {
        "nome": 'US 123 CS Prof César Montezuma',
        "endereco": 'AV CAIS DO APOLO, 925 -  BAIRRO DO RECIFE'
    },
    {
        "nome": 'US 155 CS Prof Monteiro de Morais',
        "endereco": 'AV BEBERIBE, 4510 - BEBERIBE'
    },
    {
        "nome": 'US 103 CS Prof Mário Ramos',
        "endereco": 'RUA OSCAR DE BARROS, S/Nº - CASA AMARELA'
    }
]

mensagens = []  # Stores sent messages

# Track last used ID (start from 2 since we have 1 pre-populated)
mother_id_counter = 2


def daily_pregnancy_monitor():
    today = datetime.today().date()

    for mother_id, mother in gestantes.items():
        if "inicio_gestacao" in mother:
            start_date = datetime.strptime(mother["inicio_gestacao"], "%d/%m/%Y").date()
            weeks_pregnant = (today - start_date).days // 7  # Convert days to weeks
            
            # TODO: fazer um switch com as fases da gravidez
            if weeks_pregnant <= 28: 
                #if today.month > start_date.month or (today.month == start_date.month and today.day >= start_date.day):
                # Verificar se o ano também já passou ou estamos no mesmo ano
                #if today.year > start_date.year or (today.year == start_date.year and today.month > start_date.month):
                #    print("Já faz um mês desde o início da gestação!")
                #else:
                #   print("Ainda não faz um mês desde o início da gestação.")
                pass
            elif weeks_pregnant <= 36:
                fase = 2
            else: 
                fase = 3
            # if weeks_pregnant == 10:
            #     message = f""
            #     send_mock_message(mother_id, message, "WhatsApp")

def monitor_and_send_messages():
    if mensagens:
        for msg in mensagens[:]:  # Iterate over a copy to avoid modification issues
            send_message(msg["telefone"], msg["message"])
            mensagens.remove(msg)  # Remove after sending

def forever_loop():

    last_update_id = None
    monitor_and_send_messages()
    time.sleep(1)
    daily_pregnancy_monitor()
    time.sleep(1)
    handle_updates(last_update_id)
    time.sleep(1)

# Start background threads
threading.Thread(target=forever_loop, daemon=False).start()

# def send_mock_message(mother_id, message, channel="SMS"):
#     """ Simulates sending a message via SMS or WhatsApp """
#     mensagens.append({
#         "telefone": "5581997804085",
#         "message": message,
#         "channel": channel,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     })
#     print(f"[{channel} Message] -> {message}")  # Simulate sending


@app.route('/api/mother', methods=['POST'])
def add_mother():
    """ Adds a new mother to the system (mock insert) """
    global mother_id_counter
    data = request.get_json()

    mother_id = mother_id_counter
    mother_id_counter += 1

    gestantes[mother_id] = {
        "nome": data.get("nome"),
        "inicio_gestacao": data.get("inicio_gestacao", None), 
        "primeira_consulta": data.get("primeira_consulta", time.today)
    }

    # First welcome message
    message = f"""Olá! 😊 Parabéns por iniciar o seu pré-natal! 
    Para garantir o melhor acompanhamento para você e seu bebê, é importante agendar sua próxima consulta o quanto antes.
    Aqui estão as Unidades Básicas de Saúde (UBS) mais próximas do seu endereço:
    📍 {unidades_saude[0]['nome']} – {unidades_saude[0]['endereco']}
    📍 {unidades_saude[1]['nome']} – {unidades_saude[1]['endereco']}
    📍 {unidades_saude[2]['nome']} – {unidades_saude[2]['endereco']}
    Você pode entrar em contato diretamente ou ir até a UBS mais conveniente para você e agendar sua consulta.
    Para ver a lista completa de UBS disponíveis na cidade, acesse: [🔗 Link para a lista de UBS]
    Se precisar de ajuda, estamos à disposição! 💙
    [Link do programa no Recife Conecta]"""
    mensagens.append(message)

    return jsonify({"id": mother_id, "message": "Mãe cadastrada com sucesso!"}), 201


@app.route('/api/birth', methods=['POST'])
def birth_event():
    """ Simulates a birth event and sends postpartum messages """
    data = request.get_json()
    mother_id = data.get("mae_id")
    nome_bebe = data.get("nome_bebe")

    if mother_id not in gestantes:
        return jsonify({"error": "Mãe não encontrada"}), 404

    # Simulate postpartum message
    mensagens.append(f"Parabéns pelo nascimento do bebê {nome_bebe}! Agende a consulta pós-parto.")

    return jsonify({"message": f"Notificação de nascimento enviada para {gestantes[mother_id]['nome']}"}), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
    send_message_with_keyboard()