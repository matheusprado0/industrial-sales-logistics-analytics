import pandas as pd
from sqlalchemy import create_engine
import os

print("🔄 Iniciando o processo de ETL (Extração, Transformação e Carga)...")

# 1. EXTRAÇÃO (Lendo os arquivos CSV da pasta data)
print("📥 Lendo os arquivos CSV...")
try:
    df_cliente = pd.read_csv('data/dim_cliente.csv')
    df_produto = pd.read_csv('data/dim_produto.csv')
    df_transportadora = pd.read_csv('data/dim_transportadora.csv')
    df_vendas = pd.read_csv('data/fact_vendas.csv')
    df_logistica = pd.read_csv('data/fact_logistica.csv')
    print("✅ Arquivos CSV lidos com sucesso!")
except Exception as e:
    print(f"❌ Erro ao ler os arquivos CSV. Verifique se estão na pasta 'data'. Detalhe: {e}")
    exit()

# 2. TRANSFORMAÇÃO (Ajustes de tipos e validações básicas)
print("🛠️ Tratando os tipos de dados...")
# Convertendo colunas de data para o formato datetime do pandas
df_vendas['DataVenda'] = pd.to_datetime(df_vendas['DataVenda'])
df_logistica['DataEnvio'] = pd.to_datetime(df_logistica['DataEnvio'])
df_logistica['DataEntregaPrevista'] = pd.to_datetime(df_logistica['DataEntregaPrevista'])
df_logistica['DataEntregaReal'] = pd.to_datetime(df_logistica['DataEntregaReal'])

# 3. CARGA (Conectando ao PostgreSQL e inserindo as tabelas)
# ⚠️ ATENÇÃO: Substitua 'seu_usuario', 'sua_senha' e 'IndustrialSalesAnalytics' pelos dados reais do seu Postgres
usuario = "postgres"
senha = "123"
host = "localhost"
porta = "5432"
banco = "industrialsalesanalytics"

DATABASE_URL = f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}"

try:
    print(f"🚀 Conectando ao banco de dados PostgreSQL '{banco}'...")
    engine = create_engine(DATABASE_URL)
    
    # Carregando as dimensões primeiro (para respeitar as chaves estrangeiras)
    print("📤 Carregando tabela dimcliente...")
    df_cliente.to_sql('dimcliente', engine, if_exists='replace', index=False)
    
    print("📤 Carregando tabela dimproduto...")
    df_produto.to_sql('dimproduto', engine, if_exists='replace', index=False)
    
    print("📤 Carregando tabela dimtransportadora...")
    df_transportadora.to_sql('dimtransportadora', engine, if_exists='replace', index=False)
    
    # Carregando as fatos
    print("📤 Carregando tabela factvendas...")
    df_vendas.to_sql('factvendas', engine, if_exists='replace', index=False)
    
    print("📤 Carregando tabela factlogistica...")
    df_logistica.to_sql('factlogistica', engine, if_exists='replace', index=False)
    
    print("🎉 Pipeline de ETL executado com sucesso! Todos os dados foram carregados no PostgreSQL.")

except Exception as e:
    print(f"❌ Erro ao conectar ou carregar dados no PostgreSQL: {e}")
    print("Dica: Verifique se o PostgreSQL está rodando e se o nome do banco e senha estão corretos.")