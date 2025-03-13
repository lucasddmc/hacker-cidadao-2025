from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import time
import threading
import queue
from send_message import bot
from data import *

app = Flask(__name__)
mother_id_counter = 1
def is_item_in_queue(q, item):
    """Verifica se um item já está na fila."""
    # Converte a fila em uma lista temporária para verificação
    with q.mutex:  # Usa o mutex para garantir segurança em ambientes multithread
        return item in list(q.queue)
def update_gestante(unidade, mother_id=1):
    GESTANTES[mother_id]["unidade_saude"] = UNIDADES_SAUDE[unidade]['nome']
def daily_pregnancy_monitor():
    """Check each mother's status daily and send messages if needed."""
    while True:
        today_date = datetime.today().date()
        for mother_id, mother in list(GESTANTES.items()):
            if "inicio_gestacao" in mother:
                start_date = datetime.strptime(mother["inicio_gestacao"], "%d/%m/%Y").date()
                weeks_pregnant = (today_date - start_date).days // 7
                ultima_consulta = datetime.strptime(mother["ultima_consulta"], "%d/%m/%Y").date()

                consultas_disponiveis = [
                    today_date + timedelta(days=1),
                    today_date + timedelta(days=2),
                    today_date + timedelta(days=3)
                ]

                custom_keyboard = {
                    "keyboard": [[{"text": str(date)}] for date in consultas_disponiveis],
                    "resize_keyboard": True,
                    "one_time_keyboard": True
                }

                
                if weeks_pregnant == 12 and not mother.get("sent_week_12"):
                    print("criando a mensagem")
                    message = f"""Sua gestação está avançando, e a partir de agora já é possível realizar o exame de sexagem fetal para descobrir o sexo do bebê! 🩷💙
                    Esse exame é opcional e pode ser feito a partir da 12ª semana de gestação, analisando uma amostra do seu sangue. Se tiver interesse, converse com um profissional de saúde para saber mais sobre a disponibilidade e como realizá-lo.
                    Cada fase da gestação traz novas descobertas e momentos especiais."""  
                    if not is_item_in_queue(MESSAGE_QUEUE, (message, custom_keyboard)):
                        MESSAGE_QUEUE.put((message, custom_keyboard))
                        print(f"Item adicionado: {message}")
                    else:
                        print(f"Item duplicado: {message}. Não será adicionado.")
                   
                    mother["sent_week_12"] = True  

                
                if weeks_pregnant <= 28:
                    if (today_date.year > ultima_consulta.year or 
                        (today_date.year == ultima_consulta.year and today_date.month > ultima_consulta.month)):
                        mother["ultima_consulta"] = today_date.strftime("%d/%m/%Y")
                        message = f"""Olá! 😊 Está na hora de agendar sua próxima consulta de pré-natal para garantir o melhor acompanhamento para você e seu bebê.
                        📅 De acordo com seu período gestacional, suas consultas devem ocorrer mensalmente. Escolha uma das opções abaixo para marcar sua próxima consulta:
                        1. {consultas_disponiveis[0]}
                        2. {consultas_disponiveis[1]}
                        3. {consultas_disponiveis[2]}
                        outro"""
                        MESSAGE_QUEUE.put((message, custom_keyboard))

                
                elif weeks_pregnant <= 36:
                    if today_date >= ultima_consulta + timedelta(days=15):
                        mother["ultima_consulta"] = today_date.strftime("%d/%m/%Y")
                        message = f"""Olá! 😊 Está na hora de agendar sua próxima consulta de pré-natal para garantir o melhor acompanhamento para você e seu bebê.
                        📅 De acordo com seu período gestacional, suas consultas devem ocorrer [inserir frequência: mensalmente, quinzenalmente ou semanalmente]. Escolha uma das opções abaixo para marcar sua próxima consulta:
                        1. {consultas_disponiveis[0]}\n2. {consultas_disponiveis[1]}\n3. {consultas_disponiveis[2]}
                        Caso precise de outro horário, responda com a palavra "Outro" e nossa equipe entrará em contato para mais opções.
                        Após a confirmação, você receberá um lembrete antes da consulta."""
                        MESSAGE_QUEUE.put((message, custom_keyboard))

                
                else:
                    if today_date >= ultima_consulta + timedelta(days=7):
                        mother["ultima_consulta"] = today_date.strftime("%d/%m/%Y")
                        message = f"""Olá! 😊 Está na hora de agendar sua próxima consulta de pré-natal para garantir o melhor acompanhamento para você e seu bebê.
                        📅 De acordo com seu período gestacional, suas consultas devem ocorrer [inserir frequência: mensalmente, quinzenalmente ou semanalmente]. Escolha uma das opções abaixo para marcar sua próxima consulta:
                        1. {consultas_disponiveis[0]}\n2. {consultas_disponiveis[1]}\n3. {consultas_disponiveis[2]}
                        Caso precise de outro horário, responda com a palavra "Outro" e nossa equipe entrará em contato para mais opções.
                        Após a confirmação, você receberá um lembrete antes da consulta."""
                        MESSAGE_QUEUE.put((message, custom_keyboard))

        time.sleep(86400)  


def monitor_and_send_messages():
    """Continuously process message queue."""
    while True:
        if not MESSAGE_QUEUE.empty():
            msg = MESSAGE_QUEUE.get()
            print(MESSAGE_QUEUE)
            if isinstance(msg, tuple):
                text, keyboard = msg
                bot.send_message(text, keyboard=keyboard)
            else:
                bot.send_message(msg)
            MESSAGE_QUEUE.task_done()  
        time.sleep(1)

def listen_for_updates():
    """Continuously check for Telegram updates."""
    while True:
        bot.handle_updates()
        time.sleep(1)

@app.route('/api/mother', methods=['GET'])
def get_mothers():
    """ Returns all mothers in the system """
    return jsonify(GESTANTES), 200

@app.route('/api/mother', methods=['POST'])
def add_mother():
    """ Adds a new mother to the system (mock insert) """
    global mother_id_counter
    data = request.get_json()

    mother_id = mother_id_counter
    mother_id_counter += 1

    GESTANTES[mother_id] = {
        "nome": data.get("nome"),
        "inicio_gestacao": data.get("inicio_gestacao", None), 
        "ultima_consulta": data.get("ultima_consulta", None)
    }
    custom_keyboard = {
        "keyboard": [
            [{"text": f"📍 {UNIDADES_SAUDE[0]['nome']} – {UNIDADES_SAUDE[0]['endereco']}"}],
            [{"text": f"📍 {UNIDADES_SAUDE[1]['nome']} – {UNIDADES_SAUDE[1]['endereco']}"}],
            [{"text": f"📍 {UNIDADES_SAUDE[2]['nome']} – {UNIDADES_SAUDE[2]['endereco']}"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    # First welcome message
    welcome_msg = f"""Olá, {data.get("nome")}! 😊 Parabéns por iniciar o seu pré-natal! 
    Para garantir o melhor acompanhamento para você e seu bebê, é importante agendar sua próxima consulta o quanto antes.
    Aqui estão as Unidades Saúde (US) mais próximas do seu endereço"""
    MESSAGE_QUEUE.put((welcome_msg, custom_keyboard))
    transport_msg = f"""🎉 Seu Passe Livre para Gestantes está a caminho! 🚌💙  
    Agora que você iniciou seu pré-natal, você tem direito ao Passe Livre para Gestantes, garantindo transporte gratuito no transporte público durante toda a gestação. Esse benefício facilita suas idas às consultas e exames, ajudando a garantir um acompanhamento completo para você e seu bebê.  
    📦 O vale já está a caminho da sua residência e, em alguns dias, estará em suas mãos. Fique atenta à entrega! 💙"""
    MESSAGE_QUEUE.put(transport_msg)
    return jsonify({"id": mother_id, "message": "Mãe cadastrada com sucesso!"}), 201


if __name__ == '__main__':
    # import os
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #     bot.initialize_update_id()
        
    # Start background threads
    threading.Thread(target=monitor_and_send_messages, daemon=True).start()
    threading.Thread(target=listen_for_updates, daemon=True).start()
    threading.Thread(target=daily_pregnancy_monitor, daemon=True).start()

    app.run(host="0.0.0.0", port=5001, debug=True)