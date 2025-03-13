import requests
import json
from typing import Optional, Dict, Any
from data import *
import re

class TelegramBot:
    def __init__(self, token: str, chat_id: int):
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id
        self.last_update_id: Optional[int] = None

    def _send_message(self, payload: dict, use_json: bool = True) -> bool:
        """Helper function to send messages with optional JSON payload."""
        print(self.chat_id)
        try:
            if use_json:
                response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            else:
                response = requests.post(f"{self.base_url}/sendMessage", params=payload)
            
            response.raise_for_status()
            print("Mensagem enviada com sucesso!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False

    # def send_message(self, message: str) -> bool:
    #     """Send a simple text message."""
    #     print(f"Enviando mensagem: {message}")
    #     payload = {"chat_id": self.chat_id, "text": message}
    #     return self._send_message(payload, use_json=False)

    def send_message(self, message: str, keyboard: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia uma mensagem simples ou com teclado (custom keyboard ou inline keyboard).
        
        :param message: texto da mensagem
        :param keyboard: dicionário que define o teclado (opcional). Se None, manda sem teclado.
        :return: bool indicando sucesso ou falha
        """
        print(f"Enviando mensagem: {message}")
        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        # Se um dicionário de teclado for passado, ele é incluído no payload
        if keyboard is not None:
            payload["reply_markup"] = keyboard

        # Usamos JSON quando enviamos 'reply_markup'
        use_json = keyboard is not None
        return self._send_message(payload, use_json=use_json)

    # def send_message_with_keyboard(self) -> bool:
    #     """Send persistent custom keyboard."""
    #     keyboard = {
    #         "keyboard": [
    #             [{"text": "📅 Agendar Consulta"}],
    #             [{"text": "📍 Ver UBS Mais Próxima"}],
    #             [{"text": "ℹ️ Informações sobre a Gestação"}]
    #         ],
    #         "resize_keyboard": True,
    #         "one_time_keyboard": True
    #     }
    #     payload = {
    #         "chat_id": self.chat_id,
    #         "text": "Escolha uma opção abaixo para continuar:",
    #         "reply_markup": keyboard
    #     }
    #     return self._send_message(payload)

    def get_updates(self, offset: Optional[int] = None, limit: int = 1) -> dict:
        """Fetch updates from Telegram API."""
        params = {"offset": offset, "limit": limit, "timeout": 5}
        response = requests.get(f"{self.base_url}/getUpdates", params=params)
        return response.json()

    def initialize_update_id(self) -> None:
        """Get the latest update ID on startup to avoid processing old messages."""
        updates = self.get_updates(limit=1)
        if updates.get("result"):
            self.last_update_id = updates["result"][-1]["update_id"] + 1

    def handle_updates(self) -> None:
        """Process incoming updates and respond appropriately."""
        if self.last_update_id is None:
            self.initialize_update_id()

        updates = self.get_updates(offset=self.last_update_id)
        for update in updates.get("result", []):
            current_update_id = update["update_id"]
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            response_text = "Escolha uma opção válida no menu."
            if text == "📅 Agendar Consulta":
                response_text = "Ótimo! Você pode agendar sua consulta diretamente na UBS. 📆"
            elif text == "📍 Ver UBS Mais Próxima":
                response_text = "A UBS mais próxima é a 'Unidade Saúde XYZ' 📍"
            elif text == "ℹ️ Informações sobre a Gestação":
                response_text = "Aqui estão algumas dicas para sua gestação: 🍼👶"
            elif any(nome['nome'] in text for nome in UNIDADES_SAUDE):
                response_text = "Sua unidade de saúde preferida foi salva com sucesso!"
                
                for unidade in UNIDADES_SAUDE:
                    if unidade['nome'] in text:
                        GESTANTES[1]['unidade_saude'] = unidade['nome']
                        break  # Stop checking after the first match
            elif re.match(r"^\d{4}-\d{2}-\d{2}$", text):
                response_text = f"Sua consulta foi marcada com sucesso para o dia {text}! 📅✅"
                GESTANTES[1]['consultas_marcadas'].append(text)

            #self.send_message(response_text)
            self.last_update_id = current_update_id + 1

# Initialize bot instance with credentials
#chat_id de lucas 
#bot = TelegramBot("7525923053:AAG0qW2N98Xx1FI4Pz3Be0_QNEDihnwKVqs", 1104502035)
#chat_id de ana 
bot = TelegramBot("7525923053:AAG0qW2N98Xx1FI4Pz3Be0_QNEDihnwKVqs", 6893886384)
