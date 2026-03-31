"""
analise.py
Análise de dados de atendimento ao cliente.
Gera insights sobre SLA, NPS, reincidência e performance por técnico/região.

Como executar:
    1. Execute gerar_dados.py primeiro
    2. Execute este arquivo: python analise.py
"""

import pandas as pd

# -- CARREGAMENTO DOS DADOS CRIADOS EM 'chamados.csv'  -----------------------------------------
print("=" * 30)
print("ANÁLISE DE ATENDIMENTO AO CLIENTE")
print("=" * 30)

df = pd.read_csv("dados/chamados.csv", encoding="utf-8-sig")

print(f"\n Dataset carregado: {len(df)} chamados")
print(f"Período: {df['data_abertura'].min()} até {df['data_abertura'].max()}")


# -- LIMPEZA E PREPARAÇÃO ---------------------------------------------------
# Converte todas as datas
df["data_abertura"] = pd.to_datetime(df["data_abertura"])
df["mes"] = df["data_abertura"].dt.to_period("M")
df["mes_num"] = df["data_abertura"].dt.month

# Classifica NPS (Net Promoter Score)
def classificar_nps(nota):
    if pd.isna(nota):
        return None
    if nota >= 9:
        return "Promotor"
    elif nota >= 7:
        return "Neutro"
    else:
        return "Detrator"

df["classificacao_nps"] = df["nps"].apply(classificar_nps)


# -- KPI 1 - VISÃO GERAL ---------------------------------------------------
print("\n" + "-" * 30)
print("KPI 1 - VISÃO GERAL")
print("-" * 30)

total = len(df)
resolvidos = (df["status"] == "Resolvido").sum()
em_aberto = (df["status"] == "Em aberto").sum()
cancelados = (df["status"] == "Cancelado").sum()

print(f"Total de chamados : {total}")
print(f"Resolvidos        : {resolvidos} ({resolvidos/total*100:.1f}%)")
print(f"Em aberto         : {em_aberto}  ({em_aberto/total*100:.1f}%)")
print(f"Cancelados        : {cancelados}  ({cancelados/total*100:.1f}%)")


#---- KPI 2 - CUMPRIMENTO DE SLA ---------------------------------------------------------
print("\n" + "-" * 30)
print("KPI 2 - CUMPRIMENTO DE SLA")
print("-" * 30)

sla_geral = df["dentro_sla"].mean() * 100
print(f"SLA geral cumprido: {sla_geral:.1f}%")

sla_por_categoria = (
    df.groupby("categoria")["dentro_sla"]
    .mean()
    .mul(100)
    .round(1)
    .sort_values()
    .reset_index()
)
sla_por_categoria.columns = ["Categoria", "SLA cumprido (%)"]
print(f"\n SLA por categoria:")
print(sla_por_categoria.to_string(index=False))

pior_categoria = sla_por_categoria.iloc[0]
print(f"\n Pior categoria: {pior_categoria['Categoria']} ({pior_categoria['SLA cumprido (%)']:.1f}%)")


# ----KPI 3 - NPS ---------------------------------------------------
print("\n" + "-" * 30)
print("  KPI 3 - NPS")
print("-" * 30)

df_nps = df[df["nps"].notna()].copy()

promotores = (df_nps["classificacao_nps"] == "Promotor").sum()
neutros = (df_nps["classificacao_nps"] == "Neutro").sum()
detratores = (df_nps["classificacao_nps"] == "Detrator").sum()
total_nps = len(df_nps)

nps_score = ((promotores - detratores) / total_nps) * 100

print(f"Promotores  : {promotores} ({promotores/total_nps*100:.1f}%)")
print(f"Neutros     : {neutros} ({neutros/total_nps*100:.1f}%)")
print(f"Detratores  : {detratores} ({detratores/total_nps*100:.1f}%)")
print(f"\n NPS Score   : {nps_score:.1f}")

if nps_score >= 50:
    print("Classificação: Excelente")
elif nps_score >= 0:
    print("Classificação: Zona de qualidade")
else:
    print("Classificação: Zona crítica")

nps_por_categoria = (
    df_nps.groupby("categoria")["nps"]
    .mean()
    .round(1)
    .sort_values()
    .reset_index()
)
nps_por_categoria.columns = ["Categoria", "NPS médio"]
print(f"\n NPS médio por categoria:")
print(nps_por_categoria.to_string(index=False))


# ---- KPI 4 - REINCIDÊNCIA --------------------------------------------------
print("\n" + "-" * 30)
print("KPI 4 - REINCIDÊNCIA")
print("-" * 30)

reincidencia_geral = df["reincidente"].mean() * 100
print(f"Taxa de reincidência geral: {reincidencia_geral:.1f}%")

reinc_por_cat = (
    df.groupby("categoria")["reincidente"]
    .mean()
    .mul(100)
    .round(1)
    .sort_values(ascending=False)
    .reset_index()
)
reinc_por_cat.columns = ["Categoria", "Reincidência (%)"]
print(f"\n Reincidência por categoria:")
print(reinc_por_cat.to_string(index=False))


# -- KPI 5 - PERFORMANCE POR TÉCNICO ---------------------------------------
print("\n" + "-" * 30)
print("  KPI 5 - PERFORMANCE POR TÉCNICO")
print("-" * 30)

perf_tecnico = (
    df.groupby("tecnico")
    .agg(
        total_chamados = ("id_chamado", "count"),
        sla_cumprido_pct = ("dentro_sla", lambda x: round(x.mean() * 100, 1)),
        nps_medio = ("nps", lambda x: round(x.mean(), 1)),
        reincidencia_pct = ("reincidente", lambda x: round(x.mean() * 100, 1)),
    )
    .sort_values("sla_cumprido_pct", ascending=False)
    .reset_index()
)
perf_tecnico.columns = ["Técnico", "Chamados", "SLA (%)", "NPS médio", "Reincidência (%)"]
print(perf_tecnico.to_string(index=False))


# --  INSIGHT FINAL ---------------------------------------------------------
print("\n" + "=" * 30)
print("INSIGHTS PRINCIPAIS")
print("=" * 30)

melhor_tecnico = perf_tecnico.iloc[0]["Técnico"]
pior_sla_cat = sla_por_categoria.iloc[0]["Categoria"]
maior_reinc = reinc_por_cat.iloc[0]["Categoria"]

print(f"""
  1. SLA geral de {sla_geral:.1f}% - meta recomendada: 80%+
     Categoria mais crítica: {pior_sla_cat}

  2. NPS Score de {nps_score:.1f}
     Oportunidade de melhoria em chamados de '{nps_por_categoria.iloc[0]['Categoria']}'

  3. Reincidência mais alta em '{maior_reinc}'
     Indica problema recorrente que merece análise de causa raiz

  4. Melhor performance de SLA: Técnico {melhor_tecnico}
""")

print("Análise concluída!")
