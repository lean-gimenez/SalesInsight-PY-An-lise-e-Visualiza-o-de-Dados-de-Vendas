# SalesInsight PY
 
## Sobre o projeto
Analise e visualizacao de dados de vendas desenvolvida em Python.
O projeto carrega, limpa, transforma, agrega e visualiza um dataset de vendas, gerando metricas por periodo, categoria do produto e regiao, alem de uma segmentacao simples de clientes por faixa de gasto.

## Sobre o dataset
O dataset usado nao contem uma coluna com informacao sobre produtos, mas tem a coluna categoria.
É por isso que é criada a coluna de descontos para cumprir com o RF05 (Metricas).
O dataset tem 5000 linhas e 12 colunas. As colunas:
* order_id
* order_date
* customer_id
* product_category
* region
* quantity
* unit_price
* discount
* payment method
* delivery_days
* customer_rating
* revenue

A coluna revenue é a receita, mas ainda foi criada a coluna receita_total para cumprir com RF04.

## Sobre o dataframe final
O df final tem 5000 linhas e colunas.
 
## O que o projeto analisa
- Receita total e volume de vendas por mes e por trimestre
- Top produtos e categorias por receita
- Desempenho por regiao
- Segmentacao de clientes por nivel de gasto (Bronze, Prata, Ouro)
- Relacao entre quantidade vendida e receita por transacao
- Exportacao de relatorios em CSV e JSON e de graficos em PNG
 
## Conceitos aplicados (Modulo 01 - Semanas 01 a 08)
- Logica de programacao: variaveis, tipos, operadores, condicionais
- Estruturas de dados: listas, tuplas, dicionarios e compostas
- Funcoes: parametros, retorno, lambda, ordem superior
- Leitura e escrita de arquivos CSV e JSON
- Modulo datetime e conversão de tipos (cast)
- Pandas:DataFrames, filtros, groupby, transformacoes
- Matplotlib e Seaborn: linha, barra, dispersao, subplots, export
- Git e GitHub: branches, commits e GitFlow simplificado
 
## Como executar
 
### Google Colab (recomendado)
1. Faca upload de salesinsight.py e de vendas.csv para o Colab.
2. Execute: !python salesinsight.py
3. Ou cole o conteudo em celulas de um notebook .ipynb
 
### Localmente com VS Code
1. Instale o Python 3.10+ e o VS Code.
2. Instale as dependencias:
   pip install pandas numpy matplotlib seaborn
3. Execute no terminal: python salesinsight.py
 
## Estrutura do projeto
salesinsight-py/
|-- salesinsight.py         # fluxo principal
|-- vendas.csv              # dataset (gerado ou externo)
|-- README.md
|-- outputs/
    |-- metricas_por_mes.csv
    |-- segmentacao_clientes.csv
    |-- estatisticas_gerais.json
    |-- graficos/*.png
 
## Decisoes tecnicas
Explique aqui, em poucas linhas, ao menos uma escolha que voce fez -
por exemplo, por que remover os data invalidas em vez de
mante-los.
 
## Ferramentas utilizadas
- Python 3.10+
- Google Colab / VS Code
- Bibliotecas: pandas, numpy, matplotlib, seaborn, json,
  datetime, os, random
- GitHub (e GitHub Desktop, opcional) para versionamento
- Trello / GitHub Projects para o Kanban (opcional)
 
## Video de demonstracao
[inserir o link do Google Drive ou do YouTube aqui]
