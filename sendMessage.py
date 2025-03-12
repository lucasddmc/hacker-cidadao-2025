import requests
import json


def sendMessage(telefone, message): 
    url = "https://graph.facebook.com/v22.0/575129409020264/messages"
    print(telefone)
    print(message)
    headers = {
        'Authorization': f'Bearer EAAIMpXtRPNwBO8x9w0FXoiuGjZBJE6dkMIafMZBRZAGDCNH6LLXNjwWtDsI2NlYz9XUOGIZCvUgCoZBLpyG7rLXjZAlZAunML92zdMB80dEP9RWUTIWff0qzNMQLdPMZARt3GHufOP3MS0BZAFAcgwPKLFigdgjfrsi4ZCuVmZCzvGX4kWkZCaOZAVOO1PZA93HRAcJ5qv8T9BY9ZCwpC7uoPACgY95LWJghDVImQZDZD',
        'Content-Type': 'application/json'
    }

    dados = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": 'en_US'
            }
        }
    }

    try:
        # Enviar a requisição POST
        response = requests.post(url, json=dados, headers=headers)
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            print("resposta bem sucedida")
            return response.json()  # Retorna o JSON da resposta
        else:
            print("erro no envio")
            return {"erro": f"Status code {response.status_code}", "detalhes": response.text}
    except Exception as e:
        return {"erro": str(e)}
