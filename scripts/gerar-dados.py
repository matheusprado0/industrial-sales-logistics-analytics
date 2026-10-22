import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configurando semente para reprodutibilidade dos dados
np.random.seed(42)

# Garantindo que a pasta 'data' existe para salvar os arquivos
os.makedirs('/data', exist_ok=True)

# 1. Cadastrando Clientes (Dimensão)
clientes_data = [
    (1, 'Metalúrgica Santa Rita', 'Atacado', 'Caxias do Sul', 'RS', 'Sul'),
    (2, 'Comércio de Aços Paranaense', 'Distribuidor', 'Londrina', 'PR', 'Sul'),
    (3, 'Indústria de Máquinas Alfa', 'Atacado', 'Joinville', 'SC', 'Sul'),
    (4, 'Tecnologia e Automação Ltda', 'Varejo', 'São Paulo', 'SP', 'Sudeste'),
    (5, 'Construtora e Terraplanagem Beta', 'Atacado', 'Belo Horizonte', 'MG', 'Sudeste'),
    (6, 'Equipamentos agrícolas Goiânia', 'Distribuidor', 'Goiânia', 'GO', 'Centro-Oeste'),
    (7, 'Serralheria Industrial Cuiabá', 'Varejo', 'Cuiabá', 'MT', 'Centro-Oeste'),
    (8, 'Metalúrgica Nordeste S.A.', 'Atacado', 'Recife', 'PE', 'Nordeste'),
    (9, 'Distribuidora de Insumos Bahia', 'Distribuidor', 'Salvador', 'BA', 'Nordeste')
]
df_clientes = pd.DataFrame(clientes_data, columns=['ClienteID', 'NomeCliente', 'Segmento', 'Cidade', 'Estado', 'Regiao'])

# 2. Cadastrando Produtos (Dimensão)
produtos_data = [
    (1, 'PRD-001', 'Chapa de Aço Carbono 10mm', 'Matéria-Prima', 'Chapas', 450.00, 680.00),
    (2, 'PRD-002', 'Perfil I Estrutural 6 metros', 'Matéria-Prima', 'Perfis', 890.00, 1250.00),
    (3, 'PRD-003', 'Kit Engrenagens Helicoidais', 'Componentes', 'Mecânica', 150.00, 260.00),
    (4, 'PRD-004', 'Atuador Linear Hidráulico', 'Componentes', 'Automação', 1200.00, 1850.00),
    (5, 'PRD-005', 'Correia Industrial de Transmissão', 'Componentes', 'Manutenção', 85.00, 140.00),
    (6, 'PRD-006', 'Válvula Solenóide 3 vias', 'Componentes', 'Pneumática', 320.00, 510.00),
    (7, 'PRD-007', 'Conjunto de Mancal e Rolamento', 'Componentes', 'Mecânica', 210.00, 350.00)
]
df_produtos = pd.DataFrame(produtos_data, columns=['ProdutoID', 'SKU', 'NomeProduto', 'Categoria', 'Subcategoria', 'CustoUnitario', 'PrecoBase'])

# 3. Cadastrando Transportadoras (Dimensão)
transp_data = [
    (1, 'TransLog Sul Cargas', 'Terceirizada', 'Sul'),
    (2, 'Express Via Sudeste', 'Própria', 'Sudeste'),
    (3, 'Rota Norte-Centro Rodovias', 'Terceirizada', 'Centro-Oeste'),
    (4, 'Nacional Cargas Pesadas', 'Própria', 'Nacional')
]
df_transportadoras = pd.DataFrame(transp_data, columns=['TransportadoraID', 'NomeTransportadora', 'TipoFrota', 'RegiaoAtuante'])

# 4. Gerando Vendas e Logística Simuladas (Fatos)
n_vendas = 200
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 4, 1)

vendas_list = []
logistica_list = []

for i in range(1, n_vendas + 1):
    days_offset = int(np.random.randint(0, (end_date - start_date).days))
    data_venda = start_date + timedelta(days=days_offset)
    
    cliente = df_clientes.sample(1).iloc[0]
    produto = df_produtos.sample(1).iloc[0]
    
    quantidade = int(np.random.choice([5, 10, 15, 20, 25, 30, 40, 50], p=[0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]))
    valor_unitario = float(produto['PrecoBase'])
    desconto = float(np.random.choice([0.0, 2.0, 5.0, 10.0], p=[0.6, 0.2, 0.15, 0.05]))
    
    vendas_list.append({
        'VendaID': i,
        'DataVenda': data_venda.strftime('%Y-%m-%d'),
        'ClienteID': int(cliente['ClienteID']),
        'ProdutoID': int(produto['ProdutoID']),
        'Quantidade': quantidade,
        'ValorUnitario': valor_unitario,
        'Desconto': desconto
    })
    
    transportadora = df_transportadoras.sample(1).iloc[0]
    data_envio = data_venda + timedelta(days=int(np.random.randint(1, 3)))
    prazo_entrega = int(np.random.randint(3, 8))
    data_entrega_prevista = data_envio + timedelta(days=prazo_entrega)
    
    atraso_dias = int(np.random.choice([0, int(np.random.randint(1, 5))], p=[0.8, 0.2]))
    data_entrega_real = data_entrega_prevista + timedelta(days=atraso_dias)
    status_entrega = 'No Prazo' if atraso_dias == 0 else 'Atrasado'
    
    custo_frete = round(quantidade * float(produto['CustoUnitario']) * 0.05 + float(np.random.uniform(50, 200)), 2)
    
    logistica_list.append({
        'LogisticaID': i,
        'VendaID': i,
        'TransportadoraID': int(transportadora['TransportadoraID']),
        'DataEnvio': data_envio.strftime('%Y-%m-%d'),
        'DataEntregaPrevista': data_entrega_prevista.strftime('%Y-%m-%d'),
        'DataEntregaReal': data_entrega_real.strftime('%Y-%m-%d'),
        'CustoFrete': custo_frete,
        'StatusEntrega': status_entrega
    })

df_vendas = pd.DataFrame(vendas_list)
df_logistica = pd.DataFrame(logistica_list)

# 5. Exportando para arquivos CSV dentro da pasta 'data'
df_clientes.to_csv('data/dim_cliente.csv', index=False)
df_produtos.to_csv('data/dim_produto.csv', index=False)
df_transportadoras.to_csv('data/dim_transportadora.csv', index=False)
df_vendas.to_csv('data/fact_vendas.csv', index=False)
df_logistica.to_csv('data/fact_logistica.csv', index=False)

print("Sucesso! Os arquivos CSV foram gerados e salvos na pasta 'data'.")