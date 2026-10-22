# 🏭 Industrial Sales & Logistics Analytics

Projeto corporativo de Engenharia e Business Intelligence (End-to-End) que simula o ecossistema analítico de uma empresa industrial ("Apex Industry"). O projeto cobre desde a geração de massa
de dados sintética até a modelagem relacional, consultas SQL analíticas avançadas e a entrega de um Dashboard Executivo em Power BI.

---

🛠️ Arquitetura e Fluxo de Dados
```
[ Python (Pandas / Faker) ] 
       │
       ▼ (Geração de Massa Relacional & ETL)
[ PostgreSQL (Star Schema com Integridade Referencial PK/FK) ]
       │
       ▼ (Modelagem Relacional, dCalendario & Medidas DAX)
[ Power BI (Dashboard de 3 Páginas: Executivo, Logística/OTIF e Curva ABC) ]
```

📂 Estrutura do Repositório

```
industrial-sales-analytics/
│
├── data/                    # Arquivos CSV brutos (Dimensões e Fatos)
│   ├── dim_cliente.csv
│   ├── dim_produto.csv
│   ├── dim_transportadora.csv
│   ├── fact_vendas.csv
│   └── fact_logistica.csv
│
├── database/                # Scripts de ETL e conexões
│   └── etl_pipeline.py
│
├── scripts/                 # Scripts auxiliares de automação e dados
│   └── gerar_dados.py
│
├── queries/                 # Consultas SQL analíticas e de estruturação
│   └── analysis_queries.sql
│
└── dashboard/               # Arquivos e capturas do Power BI
    └── Apex_Industrial_Analytics.pbix
```

🚀 Etapas do Desenvolvimento

1. Engenharia e Geração de Dados (Python)

   Desenvolvimento de script customizado utilizando as bibliotecas pandas e Faker para gerar transações comerciais e logísticas consistentes,
   simulando um ambiente industrial real (clientes por região/segmento,portfólio de produtos com custos e preços, e rotas de transporte).

2. Pipeline de Carga (ETL) e Banco de Dados (PostgreSQL):
   
   Tratamento e normalização dos dados estruturados.
   Carga automatizada dos arquivos CSV para o PostgreSQL via Python (SQLAlchemy / psycopg).
   
   Modelagem Dimensional (Star Schema):
   Estruturação de Tabelas Dimensão (dimcliente, dimproduto, dimtransportadora) e Tabelas Fato (factvendas, factlogistica), 
   com aplicação rígida de Chaves Primárias (PK) e Chaves Estrangeiras (FK) para integridade referencial.

3. Consultas SQL Analíticas Avançadas:

   Implementação de consultas em PostgreSQL para validação prévia de negócio:
   Margem Bruta por Categoria: Agregações complexas cruzando receita e custos operacionais.
   Performance Logística (OTIF): Mensuração de entregas no prazo utilizando condicionais (CASE WHEN).
   Curva ABC de Clientes: Utilização de Window Functions (SUM() OVER (ORDER BY ... DESC)) para cálculo dinâmico de faturamento acumulado e curva de Pareto.

4. Inteligência de Negócios e Dashboard (Power BI)

   Modelagem Relacional: Conexão estreita em estrela (1:*), criação de uma Tabela Calendário (dCalendario) dedicada
   e tratamento de relacionamentos inativos (USERELATIONSHIP)para análise temporal de logística (DataEnvio).
   Medidas DAX Avançadas: Faturamento Total, Custo Total, Lucro Bruto, Margem (%), Taxa de Pontualidade (OTIF),
   Faturamento Acumulado e Classificação Automática de Clientes (Classe A, B e C).

📊 Estrutura do Dashboard (3 Páginas)

Visão Executiva | Vendas & Margem:

   Acompanhamento de KPIs macro (Faturamento, Custo, Lucro Bruto e Margem %).
   Gráfico de evolução temporal (sazonalidade) e comparativo de desempenho por categoria de produtos (Componentes vs. Matéria-Prima).
   Tabela analítica detalhada por cliente, região e segmento.

Supply Chain | Performance Logística & OTIF:

   Monitoramento de SLA de entregas, total de entregas no prazo e custo médio de frete por transportadora.
   Filtros cruzados e análise detalhada da frota.

Inteligência Comercial | Curva ABC de Clientes:

   Aplicação do Princípio de Pareto para identificar a concentração de receita da carteira.
   Cartões estratégicos medindo o risco de concentração (ex: quantidade de clientes que sustentam 80% do faturamento) e classificação automatizada de clientes em Classes (A, Estratégico, B e C).

💻 Tecnologias Utilizadas

   Linguagens & Ferramentas: Python (Pandas, SQLAlchemy), PostgreSQL, Power BI (DAX, Modelagem Dimensional).

   Conceitos Aplicados: Star Schema, ETL, Window Functions, Gestão de Relacionamentos Ativos/Inativos, Análise de Pareto (Curva ABC) e OTIF.


<img width="6150" height="3525" alt="IndustrialSalesAnalytics_page-0001" src="https://github.com/user-attachments/assets/efef5688-9e00-460b-adee-3206a09b802b" />

<img width="6150" height="3525" alt="IndustrialSalesAnalytics_page-0002" src="https://github.com/user-attachments/assets/4815fa3c-9452-4268-ae88-d999fb01dd02" />

<img width="6150" height="3525" alt="IndustrialSalesAnalytics_page-0003" src="https://github.com/user-attachments/assets/2761d540-a313-4c9b-8039-cf6010b22e90" />

