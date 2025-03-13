from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # to get dict-like rows
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create table for mothers (gestantes)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gestantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            semana_gestacao INTEGER DEFAULT 0
        )
    """)
    # Create table for messages
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mae_id INTEGER,
            conteudo TEXT,
            canal TEXT,  -- e.g. SMS or WhatsApp
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# Initialize the database on startup
init_db()


# Endpoint to add a new mother (simulate new registration)
@app.route('/api/mother', methods=['POST'])
def add_mother():
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')
    semana_gestacao = data.get('semana_gestacao', 0)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO gestantes (nome, telefone, semana_gestacao) VALUES (?, ?, ?)",
                (nome, telefone, semana_gestacao))
    conn.commit()
    mother_id = cur.lastrowid
    conn.close()

    return jsonify({'id': mother_id, 'nome': nome, 'telefone': telefone, 'semana_gestacao': semana_gestacao}), 201



# Endpoint to list all messages (simulate notifications that would be sent)
@app.route('/api/messages', methods=['GET'])
def list_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mensagens ORDER BY created_at")
    messages = cur.fetchall()
    conn.close()

    messages_list = [dict(message) for message in messages]
    return jsonify(messages_list)


# You can add additional endpoints (for example, for birth event, post-natal follow-up, etc.)
# For example, an endpoint to simulate a birth event which triggers a post-partum message:
@app.route('/api/birth', methods=['POST'])
def birth_event():
    data = request.get_json()
    mae_id = data.get('mae_id')
    nome_bebe = data.get('nome_bebe')

    # In a real system, you would insert into a 'bebes' table and trigger actions.
    conn = get_db_connection()
    cur = conn.cursor()
    message = f"Parabéns pelo nascimento do seu bebê {nome_bebe}! Agende a consulta pós-parto para garantir os benefícios disponíveis."
    # For simplicity, we insert into messages.
    cur.execute("INSERT INTO mensagens (mae_id, conteudo, canal) VALUES (?, ?, ?)",
                (mae_id, message, "SMS"))
    conn.commit()
    conn.close()

    return jsonify({'mae_id': mae_id, 'mensagem': message}), 201


if __name__ == '__main__':
    app.run(debug=True)