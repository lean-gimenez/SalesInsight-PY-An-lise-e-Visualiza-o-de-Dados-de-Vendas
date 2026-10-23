# Importar librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# DEFINIR NOMBES DE COLUNAS AO INICIO COM CONSTANTES. 
# Colunas originais do dataset
COL_ID = 'order_id'
COL_DATA = 'order_date'
COL_CLIENTE = 'customer_id'
COL_CATEGORIA = 'product_category'
COL_REGIAO = 'region'
COL_QUANTIDADE = 'quantity'
COL_PRECO_UNIDADE = 'unit_price'
COL_DESCONTO = 'discount'
COL_PAGAMENTO = 'payment_method'
COL_DIAS_ENTREGA = 'delivery_days'

# Colunas derivadas (criadas)
COL_RECEITA = 'receita_total'
COL_MES = 'mes'
COL_MES_NOME = 'mes_nome'
COL_TRIMESTRE = 'trimestre'
COL_ANO = 'ano'
COL_FAIXA = 'faixa_receita_item'
COL_SEGMENTO = 'segmento_cliente'



# ===========================================
# === CARREGAR DATASET E TRANSFORMAR A DF ===
# ===========================================

def carregar_dados():
    dataset = "vendas.csv"
    # Transformar dataset a dataframe
    df_original = pd.read_csv(dataset)
    return df_original

df_original = carregar_dados()

# =================================
# === INSPECAO INICIAL DE DADOS ===
# =================================

def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""

    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"\nShape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")

inspecionar_dados(df_original)

# ========================
# === LIMPEZA DE DADOS ===
# ========================

def tratar_dados(df):
    """
    Trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, convertidas e finais.
    """

    # Para nao modificar o df original
    df = df.copy()

    print("\n=== LIMPEZA DE DADOS ===")

    # ESTADO INICIAL
    linhas_inicio = len(df)

    # LIMPEZA
    # 1. remover espacos extras nas colunas de texto e converter possiveis valores vazios ("") em NaN
    for col in df.select_dtypes(include=['object', 'str']).columns:
        df[col] = df[col].str.strip()
    df = df.replace("", np.nan)

    # 2. converter DATAs e descartar invalidas
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], format='%m/%d/%Y', errors='coerce')
    # Ver as datas convertidas antes de fazer metodo dropna
    convertidas = df[COL_DATA].notna().sum()
    datas_invalidas = df[COL_DATA].isna().sum()
    df = df.dropna(subset=[COL_DATA])

    # 3. Remover duplicados
    df = df.drop_duplicates()
    duplicados_removidos = linhas_inicio - len(df)

    # ESTADO FINAL
    linhas_final = len(df)

    # RELATORIO
    relatorio = {
        'Registros iniciais': linhas_inicio,
        'Registros convertidos': convertidas,
        'Registros finais': linhas_final,        
    }

    df_limpo = df
    return df_limpo, relatorio

df_limpo, relatorio = tratar_dados(df_original)

# =========================
# === COLUNAS DERIVADAS ===
# =========================

def criar_colunas(df): 
    # Copiar o df_limpo num df novo
    df = df.copy()

    # Criacao de colunas derivadas
    # Receita total
    df[COL_RECEITA] = df[COL_QUANTIDADE] * df[COL_PRECO_UNIDADE]

    # Mes
    df[COL_MES] = df[COL_DATA].dt.month

    # Nome do Mes
    meses = {
        1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril',
        5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 
        9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'
        }
    df[COL_MES_NOME] = df[COL_MES].map(meses)

    # Trimestre (no formato Q1–Q4)
    df[COL_TRIMESTRE] = "Q" + df[COL_DATA].dt.quarter.astype(str) # mudar o formato de int para str e concatenar com 'Q'

    # Ano
    df[COL_ANO] = df[COL_DATA].dt.year

    # faixa_receita_item
    # Dados extraidos dos quartis (q1 e q3)
    q1 = df[COL_RECEITA].quantile(0.25)
    q3 = df[COL_RECEITA].quantile(0.75)
    condicoes = [
        df[COL_RECEITA] < q1,
        (df[COL_RECEITA] >= q1) & (df[COL_RECEITA] < q3),
        df[COL_RECEITA] >= q3
    ]
    faixas = ['Baixo Valor', 'Medio Valor', 'Alto Valor']
    df[COL_FAIXA] = "Nao Classificado"

    for condicao, faixa in zip(condicoes, faixas):
        df.loc[condicao, COL_FAIXA] = faixa

    # VERIFICACAO
    print("")
    print("=== VERIFICACAO: NOVAS COLUNAS ===")
    novas_colunas = [COL_RECEITA, COL_MES, COL_MES_NOME, COL_TRIMESTRE, COL_ANO, COL_FAIXA]
    print(f"\nTipos de dados\n{df[novas_colunas].dtypes}")
    print(f"\nNulos\n{df[novas_colunas].isnull().sum()}")
    print(f"\nDados unicos: mes\n{df[COL_MES_NOME].unique()}")
    print(f"\nDados unicos: trimestre\n{df[COL_TRIMESTRE].unique()}")
    print(f"\nDados unicos: faixa_receita_item\n{df[COL_FAIXA].value_counts()}")
    print(f"\nAmostra do DF\n{df[novas_colunas].head()}")

    return df

df = criar_colunas(df_limpo)

# ======================
# === METRICAS DO DF ===
# ======================

# NOTA: O dataset nao contem info dos ITENS PRODUTOS, apenas as CATEGORIAS.
#       Entao vou fazer outro tipo de metrica e correlacao de variaveis.

def calcular_metricas(df):
    """
    Calcula as metricas agregadas do dataset.
    Retorna um dicionario no formato {nome_da_metrica: DataFrame}.
    """

    # Receita total, quantidade vendida e número de vendas por mês
    resumo_mensal = df.groupby([COL_MES, COL_MES_NOME]).agg(
        receita_total=(COL_RECEITA, 'sum'),
        quantidade=(COL_QUANTIDADE, 'sum'),
        n_vendas=(COL_ID, 'count')
    ).reset_index()

    # Receita total por produto (categoria) (Top 5, em ordem decrescente)
    receita_categorias = df.groupby(COL_CATEGORIA).agg(
        receita_total=(COL_RECEITA, 'sum')
    ).reset_index()
    top_categorias = receita_categorias.sort_values(by=COL_RECEITA, ascending=False).head()

    # Receita total e ticket médio por região.
    receita_regiao = df.groupby(COL_REGIAO).agg(
        receita_total=(COL_RECEITA, 'sum'),
        ticket_medio=(COL_RECEITA, 'mean')
    ).reset_index()

    # Desconto por metodo de pago
    metodo_categoria_desconto = df.groupby([COL_PAGAMENTO, COL_CATEGORIA]).agg(
        vendas_com_desconto=(COL_DESCONTO, 'count')
    ).reset_index()

    metricas = {
        "POR MÊS": resumo_mensal,
        "TOP CATEGORIAS": top_categorias,
        "POR REGIÃO": receita_regiao,
        "DESCONTO POR PAGAMENTO E CATEGORIA": metodo_categoria_desconto,
    }

    return metricas

metricas = calcular_metricas(df)

def resumo(dict):
    print()
    for titulo, tabela in dict.items():
        print(f"\n=== {titulo} ===")
        print(tabela.to_string(index=False))

resumo = resumo(metricas)

# ===============================
# === SEGMENTACAO DE CLIENTES ===
# ===============================

def segmentar_clientes(df):
    """
    Agrupa por cliente, soma a receita 
    e classifica em Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento.
    """

    # Agrupar por cliente e receita. Renomear colunas.
    clientes = (
        df.groupby(COL_CLIENTE)[COL_RECEITA]
        .sum()
        .reset_index()
        .rename(columns={COL_CLIENTE:'cliente', COL_RECEITA:'total_gasto'})
    )

    clientes['segmento'] = clientes['total_gasto'].apply(
        lambda x: 'Bronze' if x < 5000 else ('Prata' if x <= 15000 else 'Ouro')
    )

    print("\nTOP 10 CLIENTES")
    top10_clientes = clientes.sort_values(by='total_gasto', ascending=False).head(10)
    print(top10_clientes.to_string(index=False))

    # DISTRIBUICAO POR SEGMENTO
    resumo_segmento = clientes.groupby('segmento').agg(
        n_clientes=('cliente', 'count'),
        total_gasto=('total_gasto', 'sum'),
    )
    resumo_segmento['%_clientes'] = (resumo_segmento['n_clientes'] / resumo_segmento['n_clientes'].sum() * 100).round(1)
    resumo_segmento['%_gasto'] = (resumo_segmento['total_gasto'] / resumo_segmento['total_gasto'].sum() * 100).round(1)

    ordem = ['Bronze', 'Prata', 'Ouro']

    print("\nDISTRIBUICAO POR SEGMENTO")
    print(clientes['segmento'].value_counts().reindex(ordem))
    print()
    print(resumo_segmento.reindex(ordem))

    return clientes

segmentar_clientes(df)