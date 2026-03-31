# Análise de Atendimento ao Cliente

Projeto de análise de dados simulando o contexto real de uma central de atendimento técnico. O objetivo é extrair KPIs operacionais — SLA, NPS, reincidência e performance por técnico — a partir de um dataset de chamados.

---

## Problema de negócio

Centrais de atendimento técnico precisam monitorar constantemente a qualidade do serviço. Perguntas que este projeto responde:

- Qual o percentual de chamados resolvidos dentro do SLA contratado?
- Qual categoria de problema tem o pior desempenho?
- Como está o NPS dos clientes atendidos?
- Quais técnicos têm melhor performance?
- Onde a reincidência de problemas é mais alta?

---

## Tecnologias utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-217346?style=flat&logo=microsoftexcel&logoColor=white)

---

## Estrutura do projeto

```
projeto-atendimento-clientes/
│
├── dados/
│   └── chamados.csv        # dataset gerado (500 chamados fictícios)
├── gerar_dados.py          # gera o dataset com faker/random
├── analise.py              # análise principal com KPIs
└── README.md
```

---

## ▶ Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/projeto-atendimento-clientes.git
cd projeto-atendimento-clientes
```

**2. Instale a dependência**

```bash
pip install pandas
```

**3. Gere o dataset**

```bash
python gerar_dados.py
```

**4. Execute a análise**

```bash
python analise.py
```

---

## Principais resultados

| KPI                        | Resultado            |
| -------------------------- | -------------------- |
| SLA geral cumprido         | ~68%                 |
| NPS Score                  | Zona de qualidade    |
| Categoria com pior SLA     | Peça com defeito     |
| Maior taxa de reincidência | Falha técnica (~30%) |

> Os dados são fictícios e gerados com distribuições baseadas em cenários reais de atendimento técnico industrial.

---

## Próximos passos

- [ ] Visualizações com matplotlib/seaborn
- [ ] Dashboard em Power BI conectado ao CSV
- [ ] Análise de tendência mensal de SLA

---

_Projeto desenvolvido por [Vinicius Degelo](https://linkedin.com/in/vinicius-degelo) como parte do portfólio de Análise de Dados._
