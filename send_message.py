import requests
import json

# TOKEN = "EAAIMpXtRPNwBOy4sG45ZAEOhulr3sns5lo6vgBO6gBFe7vVPddEsHr2NhHkHxHlP9HngaC1VIHdrTMVZCqyEWkVvEvNoGL6It5P8E6cE6evZCZCS4CU2cxHv0dEKcLKuFmLZCr4vgNJDiaBPekxdsE2JgvWVMs4XXnvtlGf7CXlVdAGzzgmKZAOkcvn2fUqLGq05qxIJUzltUGXMPfxqcT6WKDuWwZD"

def send_message(telefone, message):
    url = f"https://api.telegram.org/bot7525923053:AAG0qW2N98Xx1FI4Pz3Be0_QNEDihnwKVqs/sendMessage"
    params = {"chat_id": 1104502035, "text": message}
    print("executou")
    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.text}")

    