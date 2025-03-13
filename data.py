from datetime import datetime, timedelta
import queue

today = datetime.today().date()

CONSULTAS_DISPONIVEIS = [
    today + timedelta(days=1),
    today + timedelta(days=2),
    today + timedelta(days=3)
]

# Configuration
MESSAGE_QUEUE = queue.Queue()
GESTANTES = {
    1: {
        "nome": "Ana Souza",
        "telefone": "+5581999999999",
        "inicio_gestacao": "19/12/2024", 
        "ultima_consulta": "13/02/2025",
        "unidade_saude": ""
    }
}
UNIDADES_SAUDE = [
    {"nome": 'US 123 CS Prof César Montezuma', "endereco": 'AV CAIS DO APOLO, 925 - BAIRRO DO RECIFE'},
    {"nome": 'US 155 CS Prof Monteiro de Morais', "endereco": 'AV BEBERIBE, 4510 - BEBERIBE'},
    {"nome": 'US 103 CS Prof Mário Ramos', "endereco": 'RUA OSCAR DE BARROS, S/Nº - CASA AMARELA'}
]