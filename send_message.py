import requests
import json
import time

url = f"https://api.telegram.org/bot7525923053:AAG0qW2N98Xx1FI4Pz3Be0_QNEDihnwKVqs/sendMessage"
chat_id = 1104502035

def send_message(message):
    params = {"chat_id": chat_id, "text": message}
    print("mensagem" + message)
    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.text}")


def send_message_with_buttons(message):
    print("mensagem" + message)
    # Inline buttons (can be clicked)
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔗 Ver UBS Disponíveis", "url": "https://www.recife.pe.gov.br/geoescolas"}],
            [{"text": "📅 Agendar Consulta", "callback_data": "schedule_consultation"}]
        ]
    }
 
    payload = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": json.dumps(keyboard)
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.text}")

def send_message_with_keyboard():
    
    keyboard = {
        "keyboard": [
            [{"text": "📅 Agendar Consulta"}],
            [{"text": "📍 Ver UBS Mais Próxima"}],
            [{"text": "ℹ️ Informações sobre a Gestação"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    payload = {
        "chat_id": chat_id,
        "text": "Escolha uma opção abaixo para continuar:",
        "reply_markup": json.dumps(keyboard)
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.text}")


def get_updates(offset=None):
    params = {"offset": offset, "timeout": 5}
    response = requests.get(url + "/getUpdates", params=params)
    return response.json()

def handle_updates(last_update_id):
    updates = get_updates(last_update_id)
    for update in updates.get("result", []):
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]  # User message (button text)

        if text == "📅 Agendar Consulta":
            response_text = "Ótimo! Você pode agendar sua consulta diretamente na UBS. 📆"
        elif text == "📍 Ver UBS Mais Próxima":
            response_text = "A UBS mais próxima é a 'Unidade Saúde XYZ' 📍"
        elif text == "ℹ️ Informações sobre a Gestação":
            response_text = "Aqui estão algumas dicas para sua gestação: 🍼👶"
        else:
            response_text = "Escolha uma opção válida no menu."

        # Send response
        requests.post(url + "/sendMessage", json={"chat_id": chat_id, "text": response_text})

        last_update_id = update["update_id"] + 1