import sqlite3
import json
import sendMessage as sm
from datetime import datetime, timedelta

# Conexão com banco de dados SQLite em memória
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# Criação das tabelas
cur.execute("""
CREATE TABLE gestantes (
    cpf TEXT PRIMARY KEY, 
    nome TEXT,
    telefone TEXT,
    endereco TEXT, 
    semana_gestacao INTEGER DEFAULT 0, 
    quantidade_consultas INTEGER DEFAULT 0
)""")
cur.execute("""
CREATE TABLE bebes (
    id INTEGER PRIMARY KEY,
    cpf TEXT,
    mae_id INTEGER,
    nome TEXT,
    data_nascimento TEXT,
    vivo INTEGER
)""")
cur.execute("""
CREATE TABLE consultas (
    id INTEGER PRIMARY KEY,
    mae_id INTEGER,
    bebe_id INTEGER,
    data TEXT,
    descricao TEXT,
    lembrete_enviado INTEGER DEFAULT 0
)""")
cur.execute("""
CREATE TABLE mensagens (
    id INTEGER PRIMARY KEY,
    mae_id INTEGER, 
    conteudo TEXT,
    canal TEXT
)""")
cur.execute("""
CREATE TABLE UBS(
    id INTEGER PRIMARY KEY,
    nome TEXT, 
    endereco TEXT
)""")

# Triggers para marcos da gravidez (3 meses e 6 meses)

#cur.execute("""
#CREATE TRIGGER marco_3_meses
#AFTER UPDATE ON gestantes
#WHEN new.semana_gestacao >= 12 AND old.semana_gestacao < 12
#BEGIN
#   INSERT INTO mensagens(mae_id, conteudo, canal)
#    VALUES (
#        new.id,
#        'Parabéns! Você completou 3 meses de gravidez. Aproveite os exames pré-natais gratuitos e cuide bem da sua saúde.',
#        'SMS'
#    );
#END;
#""") 
cur.execute("""
CREATE TRIGGER marco_6_meses
AFTER UPDATE ON gestantes
WHEN new.semana_gestacao >= 24 AND old.semana_gestacao < 24
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.id,
        'Você atingiu 6 meses de gravidez! Continue se preparando para o parto. Lembre-se de seus direitos, como licença-maternidade em breve.',
        'WhatsApp'
    );
END;
""")

# Trigger para evento de nascimento do bebê (pós-parto)
cur.execute("""
CREATE TRIGGER evento_nascimento
AFTER INSERT ON bebes
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.mae_id,
        'Parabéns pelo nascimento do seu bebê ' || new.nome || '! Agende a consulta pós-parto e registre o bebê para ter acesso aos benefícios, como a licença-maternidade.',
        'SMS'
    );
END;
""")

# Triggers para marcos do bebê (6 meses e 12 meses de vida)
cur.execute("""
CREATE TRIGGER bebe_6_meses
AFTER UPDATE ON bebes
WHEN new.idade_meses >= 6 AND old.idade_meses < 6
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.mae_id,
        'Seu bebê ' || new.nome || ' completou 6 meses! Não se esqueça das vacinas desta idade e do acompanhamento pediátrico gratuito no posto de saúde.',
        'WhatsApp'
    );
END;
""")
cur.execute("""
CREATE TRIGGER bebe_12_meses
AFTER UPDATE ON bebes
WHEN new.idade_meses >= 12 AND old.idade_meses < 12
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.mae_id,
        'Seu bebê ' || new.nome || ' fez 1 aninho! Leve-o ao pediatra para um check-up e mantenha as vacinas em dia – todos disponíveis gratuitamente.',
        'WhatsApp'
    );
END;
""")

# Triggers para lembretes de consultas (mãe e bebê)
cur.execute("""
CREATE TRIGGER lembrete_consulta_mae
AFTER UPDATE ON consultas
WHEN new.lembrete_enviado = 1 AND old.lembrete_enviado = 0 AND new.bebe_id IS NULL
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.mae_id,
        'Lembrete: Amanhã você tem uma consulta marcada: ' || new.descricao || '. Não falte!',
        'SMS'
    );
END;
""")
cur.execute("""
CREATE TRIGGER lembrete_consulta_bebe
AFTER UPDATE ON consultas
WHEN new.lembrete_enviado = 1 AND old.lembrete_enviado = 0 AND new.bebe_id IS NOT NULL
BEGIN
    INSERT INTO mensagens(mae_id, conteudo, canal)
    VALUES (
        new.mae_id,
        'Lembrete: Amanhã seu bebê ' || (SELECT nome FROM bebes WHERE id = new.bebe_id) || ' tem uma consulta: ' || new.descricao || '. Não falte!',
        'SMS'
    );
END;
""")

conn.commit()

# Inserção de uma gestante fictícia
cur.execute("INSERT INTO gestantes (nome, telefone, semana_gestacao) VALUES (?, ?, ?)",
            ("Maria", "5581997804085", 0)) # salvo com o numero de lucas 

# Atualização da semana de gestação para simular marcos:
cur.execute("UPDATE gestantes SET semana_gestacao = 12 WHERE nome = 'Maria'")   # 12 semanas (3 meses)
cur.execute("UPDATE gestantes SET semana_gestacao = 24 WHERE nome = 'Maria'")   # 24 semanas (6 meses)

# Inserção de um bebê (simula o parto/nascimento)
cur.execute("INSERT INTO bebes (mae_id, nome, data_nascimento, idade_meses) VALUES (?, ?, ?, ?)",
            (1, "João", "2025-03-12", 0))

# Atualização da idade do bebê para simular crescimento:
cur.execute("UPDATE bebes SET idade_meses = 6 WHERE nome = 'João'")   # Bebê chega a 6 meses
cur.execute("UPDATE bebes SET idade_meses = 12 WHERE nome = 'João'")  # Bebê chega a 12 meses (1 ano)

# Agendamento de uma consulta (ex: consulta pediátrica futura)
data_hoje = datetime.now().date()
data_amanha = data_hoje + timedelta(days=1)
cur.execute("INSERT INTO consultas (mae_id, bebe_id, data, descricao, lembrete_enviado) VALUES (?, ?, ?, ?, ?)",
            (1, 1, data_amanha.isoformat(), "Consulta pediátrica de rotina", 0))

# Simulação do envio de lembrete um dia antes da consulta (marcando lembrete_enviado = 1)
cur.execute("UPDATE consultas SET lembrete_enviado = 1 WHERE data = ? AND lembrete_enviado = 0",
            (data_amanha.isoformat(),))
conn.commit()

# Consulta à tabela de mensagens para obter todas as mensagens geradas
cur.execute("SELECT canal, conteudo, mae_id FROM mensagens ORDER BY id")
mensagens_geradas = cur.fetchall()

for canal, conteudo, mae_id in mensagens_geradas:
    cur.execute("SELECT telefone FROM gestantes WHERE id = ?", (mae_id,)) 
    telefone = cur.fetchone()
    if telefone:  
        sm.sendMessage(telefone[0], conteudo)
    else: 
        print("id da mãe não encontrado")

