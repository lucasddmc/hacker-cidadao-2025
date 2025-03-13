import requests
import pywhatkit
import json

# TOKEN = "EAAIMpXtRPNwBOy4sG45ZAEOhulr3sns5lo6vgBO6gBFe7vVPddEsHr2NhHkHxHlP9HngaC1VIHdrTMVZCqyEWkVvEvNoGL6It5P8E6cE6evZCZCS4CU2cxHv0dEKcLKuFmLZCr4vgNJDiaBPekxdsE2JgvWVMs4XXnvtlGf7CXlVdAGzzgmKZAOkcvn2fUqLGq05qxIJUzltUGXMPfxqcT6WKDuWwZD"

def send_message(telefone, message):
    # url = "https://graph.facebook.com/v22.0/575129409020264/messages"
    print(telefone)
    print(message)
    pywhatkit.start_server(port=8000, print_msg=True)
    pywhatkit.sendwhatmsg_instantly("+5581997566939", "iaiiii ana paula", 0)
    # headers = {
    #     'Authorization': f'Bearer {TOKEN}',
    #     'Content-Type': 'application/json'
    # }
    #
    # dados = {
    #     "messaging_product": "whatsapp",
    #     "to": telefone,
    #     "type": "template",
    #     "template": {
    #         "name": "Prefeitura do recife",
    #         "language": {
    #             "code": 'en_US'
    #         }
    #     }
    # }
    #
    # try:
    #     # Enviar a requisição POST
    #     response = requests.post(url, json=dados, headers=headers)
    #     # Verificar se a requisição foi bem-sucedida
    #     if response.status_code == 200:
    #         print("resposta bem sucedida")
    #         return response.json()  # Retorna o JSON da resposta
    #     else:
    #         print("erro no envio")
    #         return {"erro": f"Status code {response.status_code}", "detalhes": response.text}
    # except Exception as e:
    #     return {"erro": str(e)}
