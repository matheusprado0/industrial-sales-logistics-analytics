-- =========================================================================
-- PROJETO: Industrial Sales & Logistics Analytics
-- ARQUIVO: 04_analysis_queries.sql
-- DESCRIÇÃO: Consultas analíticas avançadas para portfólio (SQL / PostgreSQL)
-- =========================================================================

-- 1. Faturamento Total, Quantidade Vendida e Margem Bruta por Categoria de Produto
-- Esta query analisa o desempenho financeiro por categoria, calculando a receita bruta e o lucro estimado.
SELECT 
    p."Categoria",
    COUNT(DISTINCT v."VendaID") AS TotalPedidos,
    SUM(v."Quantidade") AS QtdTotalVendida,
    SUM(v."Quantidade" * v."ValorUnitario") AS FaturamentoBruto,
    SUM(v."Quantidade" * p."CustoUnitario") AS CustoTotal,
    SUM(v."Quantidade" * v."ValorUnitario") - SUM(v."Quantidade" * p."CustoUnitario") AS LucroBruto,
    ROUND(
        (
            (SUM(v."Quantidade" * v."ValorUnitario") - SUM(v."Quantidade" * p."CustoUnitario")) 
            / NULLIF(SUM(v."Quantidade" * v."ValorUnitario"), 0)
        )::numeric, 4
    ) * 100 AS MargemPercentual
FROM factvendas v
JOIN dimproduto p ON v."ProdutoID" = p."ProdutoID"
GROUP BY p."Categoria"
ORDER BY FaturamentoBruto DESC;


-- 2. Performance Logística e Nível de Serviço por Transportadora (OTIF / Atrasos)
-- Crucial para indústrias medirem a eficiência das entregas e o impacto dos fretes.
-
SELECT 
    t."NomeTransportadora",
    t."TipoFrota",
    COUNT(l."LogisticaID") AS TotalEntregas,
    SUM(CASE WHEN l."StatusEntrega" = 'No Prazo' THEN 1 ELSE 0 END) AS EntreguesNoPrazo,
    SUM(CASE WHEN l."StatusEntrega" = 'Atrasado' THEN 1 ELSE 0 END) AS EntreguesComAtraso,
    ROUND(
        ((SUM(CASE WHEN l."StatusEntrega" = 'No Prazo' THEN 1 ELSE 0 END) * 100.0) / COUNT(l."LogisticaID"))::numeric, 2
    ) AS TaxaPontualidadePercentual,
    ROUND(AVG(l."CustoFrete")::numeric, 2) AS CustoMedioFrete
FROM factlogistica l
JOIN dimtransportadora t ON l."TransportadoraID" = t."TransportadoraID"
GROUP BY t."NomeTransportadora", t."TipoFrota"
ORDER BY TaxaPontualidadePercentual DESC;


-- 3. Curva ABC de Clientes (Faturamento Acumulado)
-- Classifica os clientes por relevância de faturamento usando Window Functions (Funções de Janela).
WITH FaturamentoClientes AS (
    SELECT 
        c."NomeCliente",
        c."Segmento",
        c."Regiao",
        SUM(v."Quantidade" * v."ValorUnitario") AS FaturamentoTotal
    FROM factvendas v
    JOIN dimcliente c ON v."ClienteID" = c."ClienteID"
    GROUP BY c."NomeCliente", c."Segmento", c."Regiao"
)
SELECT 
    "NomeCliente",
    "Segmento",
    "Regiao",
    ROUND(FaturamentoTotal::numeric, 2) AS FaturamentoTotal,
    ROUND(
        (SUM(FaturamentoTotal) OVER (ORDER BY FaturamentoTotal DESC) * 100.0 / SUM(FaturamentoTotal) OVER ())::numeric, 2
    ) AS FaturamentoAcumuladoPercentual
FROM FaturamentoClientes
ORDER BY FaturamentoTotal DESC;