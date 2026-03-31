"""
gerar_dados.py
Gera um dataset fictício de chamados de atendimento ao cliente.
Execute este arquivo primeiro para criar o arquivo dados/chamados.csv
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Garante que a pasta 'dados' existe
os.makedirs("dados", exist_ok=True)

# Semente para resultados reproduzíveis
random.seed(42)
np.random.seed(42)

# -- Configurações do dataset --------------------------------------------------
N_CHAMADOS = 500

CATEGORIAS = ["Manutenção preventiva", "Falha técnica", "Dúvida de uso", "Instalação", "Peça com defeito"]
STATUS = ["Resolvido", "Resolvido", "Resolvido", "Em aberto", "Cancelado"]  # mais resolvidos = realista
TECNICOS = ["Carlos", "Ana", "Roberto", "Fernanda", "Lucas"]
REGIOES = ["São Paulo", "Campinas", "Ribeirão Preto", "Santos", "Sorocaba"]
CANAIS = ["Telefone", "E-mail", "App", "Presencial"]

DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

# -- Geração dos dados ---------------------------------------------------------
chamados = []

for i in range(1, N_CHAMADOS + 1):
    abertura = DATA_INICIO + timedelta(
        days=random.randint(0, (DATA_FIM - DATA_INICIO).days)
    )

    categoria = random.choice(CATEGORIAS)
    status = random.choice(STATUS)
    canal = random.choice(CANAIS)

    # SLA em horas varia por categoria (falha técnica demora mais)
    sla_base = {
        "Manutenção preventiva": 48,
        "Falha técnica": 72,
        "Dúvida de uso": 24,
        "Instalação": 36,
        "Peça com defeito": 96,
    }
    sla_horas = sla_base[categoria]

    # Tempo real de resolução: alguns dentro do SLA, outros não
    dentro_sla = random.random() < 0.68  # 68% dentro do SLA
    horas_offset = random.uniform(-12, 24) if dentro_sla else random.uniform(24, 72)
    tempo_resolucao = round(sla_horas + horas_offset, 1)

    # NPS só para chamados resolvidos
    nps = random.randint(0, 10) if status == "Resolvido" else None

    # Reincidência: falhas técnicas reincidem mais
    reincidente = random.random() < (0.3 if categoria == "Falha técnica" else 0.1)

    chamados.append({
        "id_chamado": f"CH{i:04d}",
        "data_abertura": abertura.strftime("%Y-%m-%d"),
        "categoria": categoria,
        "canal": canal,
        "tecnico": random.choice(TECNICOS),
        "regiao": random.choice(REGIOES),
        "status": status,
        "tempo_resolucao_h": tempo_resolucao,
        "sla_contratado_h": sla_horas,
        "dentro_sla": dentro_sla,
        "reincidente": reincidente,
        "nps": nps,
    })

df = pd.DataFrame(chamados)
df.to_csv("dados/chamados.csv", index=False, encoding="utf-8-sig")

print(f"Dataset gerado com sucesso: {N_CHAMADOS} chamados")
print(f"Arquivo salvo em: dados/chamados.csv")
print(f"\n Primeiras linhas:")
print(df.head(3).to_string(index=False))
