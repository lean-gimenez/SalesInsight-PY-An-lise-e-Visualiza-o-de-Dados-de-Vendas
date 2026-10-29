# SalesInsight PY
 
## Sobre o projeto
Analise e visualizacao de dados de vendas desenvolvida em Python.
O projeto carrega, limpa, transforma, agrega e visualiza um dataset de vendas, gerando metricas por periodo, categoria do produto e regiao, alem de uma segmentacao simples de clientes por faixa de gasto.

## Sobre o dataset
O dataset usado nao contem uma coluna com informacao sobre produtos, mas tem a coluna categoria.
É por isso que é criada a coluna de descontos para cumprir com o RF05 (Metricas).
Além disso, o dataset é sintético, pois tem dados desde 2022 até 2035.

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

A coluna revenue é a receita. Mesmo assim, a coluna receita_total foi criada para cumprir com RF04.

## Sobre o dataframe final
O df final tem 5000 linhas e 18 colunas.

Colunas criadas
* 'receita_total'
* 'mes'
* 'mes_nome'
* 'trimestre'
* 'ano'
* 'faixa_receita_item'
 
## O que o projeto analisa
- Receita total e volume de vendas por mes e por trimestre
- Top produtos e categorias por receita
- Desempenho por regiao
- Segmentacao de clientes por nivel de gasto (Bronze, Prata, Ouro)
- Relacao entre quantidade vendida e receita por transacao
- Exportacao de relatorios em CSV e JSON e de graficos em PNG

## Insights gerados
* Maio e agosto são os meses com maior receita. 
* Os meses que menos recaudaram são abril, setembro, outubro, novembro e dezembro.
* Os produtos eletrônicos foram os mais consumidos.
* Não tem diferenças importantes entre o desempenho entre trimestres nem entre regiões.
* Os últimos trimestres de 2030 e 2033 tem a maior projeção de vendas.
* Os produtos de Baixo Valor apenas participam na receita. São mais consumidos os produtos de Alto Valor e, em segundo lugar, os de Médio Valor.
* Os clientes Prata (nível intermédio de participação da receita total) são o grupo mais grande.

## Como acionar
* É recomendável incrementar a promoção dos produtos eletrônicos de Valor Alto e Médio.
* Fazer a promoção para o último cuatrimestre do ano. 
* Poderiam se incluir descontos para datas específicas: feriados de setembro até dezembro, dias 09/09, 10/10, 11/11 e 12/12, dia da primavera, dia do maestro, halloween, natal, réveillon.
* Começar uma campanha de fidelidade com novos clientes que ingresaram em abril, especialmente por Páscoa e São Jorge.
 
## Conceitos aplicados
- Logica de programacao: variaveis, tipos, operadores, condicionais
- Estruturas de dados: listas, tuplas, dicionarios e compostas
- Funcoes: parametros, retorno, lambda, ordem superior
- Leitura e escrita de arquivos CSV e JSON
- Modulo datetime e conversao de tipos
- Pandas: DataFrames, filtros, groupby, transformacoes
- Matplotlib e Seaborn: linha, barra, dispersao, subplots, export
- Git e GitHub: branches, commits e GitFlow simplificado
 
## Como executar
 
### Google Colab
1. Faca upload de salesinsight.py e de vendas.csv para o Colab.
    a. Acesse o Google Colab e crie um novo notebook.
    b. No painel esquerdo, faça o upload dos arquivos 'salesinsight.py' e 'vendas.csv'.
2. Execute: !python salesinsight.py.
3. Ou cole o conteudo em celulas de um notebook .ipynb.
4. Graficos:
    a. Revise a pasta outputs/graficos para ver os graficos guardados. Especialmente, 'painel_resumo.png'.
    b. Pode encontrar também os arquivos csv e json sobre estatisticas.
 
### Localmente com VS Code
1. Instale o Python 3.10+ e o VS Code.
2. Instale as dependencias:
   * Na consola escreva
        + pip install -r requirements.txt
3. Execute no terminal: python salesinsight.py
 
## Estrutura do projeto
salesinsight-py/
|-- salesinsight.py         # fluxo principal
|-- vendas.csv              # dataset externo
|-- README.md               
|-- requirements.txt
|-- outputs/
    |-- metricas_por_mes.csv
    |-- segmentacao_clientes.csv
    |-- estatisticas_gerais.json
    |-- graficos/
        |-- distribuicao_segmentos.png
        |-- matriz_correlacao_trimestral.png
        |-- painel_resumo_extra.png
        |-- painel_resumo.png
        |-- quantidade_vs_receita.png
        |-- receita_por_mes.png
        |-- receita_por_regiao.png
        |-- receita_por_trimestre.png
        |-- top_categorias.png
        |-- vendas_por_faixa_preco.png
 
## Decisoes tecnicas
* Datas
As datas foram convertidas com to_datetime

* Constantes
Os nomes das colunas e os limites dos segmentos Prata e Ouro foram declarados em constantes ao inicio para ser reutilizados. 

* Faixas receita
Para determinar as categorias de Baixo Valor, Medio Valor e Alto Valor, foi usada a informacao dos quartis 1ro e 3ro. Com isso o Medio Valor corresponde aos items com receitas entre o quartil 1 e o quartil 3.  

* Utilizar a coluna categoria em lugar do produto porque o dataset não tem nomes de produtos. 

* Criação da métrica Vendas por Desconto em 3 faixas
    - <10%, 10-20%, >20%

* Uso dos quartis da receita para estabelecer as faixas e segmentar os clientes:
    - q1 = clientes['total_gasto'].quantile(0.25)
      q3 = clientes['total_gasto'].quantile(0.75)
      lambda x: 'Bronze' if x < q1 else ('Prata' if x <= q3 else 'Ouro')


## Ferramentas utilizadas
- Python 3.10+
- VS Code
- Bibliotecas: pandas, numpy, matplotlib, seaborn, json, datetime, os, random
- GitHub para versionamento
- GitHub Projects para o Kanban
 
## Video de demonstracao
https://drive.google.com/file/d/1mdx7dNt-B6_stKLGyoTnyQE4el5KTKBU/view?usp=sharing

## Kanban
https://github.com/users/lean-gimenez/projects/1

## Aspectos para melhorar
* Modularização de funções e do código
    - Fazer diferentes arquivos .py e importar eles como módulos ao .py principal.
    - Evitar repetições no código. Por exemplo:
        print
        fig, ax = plt.subplots()

* Implementar try/except para validar dados e capturar exeções específicas.
