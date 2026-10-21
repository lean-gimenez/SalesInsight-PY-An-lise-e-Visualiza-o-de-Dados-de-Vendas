# Importar librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dataset e transformar a dataframe
def carregar_dados():
    dataset = "vendas.csv"
    # Transformar dataset a dataframe
    df_original = pd.read_csv(dataset)
    return df_original

df_original = carregar_dados()


# Inspecao inicial de dados
def inspecao_inicial(df):
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"\nShape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return

inspecao_inicial(df_original)


# Limpeza de dados
def tratar_dados(df):
    # Para nao modificar o df original
    df = df.copy()
    print("\n=== LIMPEZA DE DADOS ===")
    # ESTADO INICIAL (ANTES DA LIMPEZA)
    linhas_inicio = len(df)
    duplicados_inicio = df.duplicated().sum()

    # LIMPEZA
    # 1. remover espacos extras nas colunas de texto
    for col in df.select_dtypes(include=['object', 'str']).columns:
        df[col] = df[col].str.strip()
    # Converter possiveis valores vazios ("") em NaN
    df = df.replace("", np.nan)

    # 2. converter order_date e descartar datas invalidas
    df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')
    datas_invalidas = df["order_date"].isna().sum()
    df = df.dropna(subset=['order_date'])

    # 3. Remover duplicados
    df = df.drop_duplicates()

    # ESTADO FINAL (POST LIMPEZA)
    linhas_final = len(df)
    duplicados_final = df.duplicated().sum()

    # RELATORIO
    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Linhas antes: {linhas_inicio}")
    print(f"Linhas depois: {linhas_final}")
    print(f"Linhas removidas: {linhas_inicio - linhas_final}")
    print("Sem Nulos")
    print("Sem Duplicados")
    print(f"Datas inválidas removidas: {datas_invalidas}")
    print("DATAFRAME LIMPO:")
    print(f"{df.head()}")
    return df

df_limpo = tratar_dados(df_original)

# ANALISE DE METRICAS

# Copiar o df_limpo num df novo
df = df_limpo.copy()

# Criacao de colunas derivadas
# Receita total
df['receita_total'] = df['quantity'] * df['unit_price']

# Mes
df['mes'] = df['order_date'].dt.month

# Nome do Mes
meses = {
    1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril',
    5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 
    9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'
    }
df['mes_nome'] = df['mes'].map(meses)

# Trimestre (no formato Q1–Q4)
df['trimestre'] = "Q" + df['order_date'].dt.quarter.astype(str) # mudar o formato de int para str e concatenar com 'Q'

# Ano
df['ano'] = df['order_date'].dt.year

# faixa_receita_item
# Dados extraidos dos quartis (Q1 = 440.762500, Q2 = 984.740000, Q3 = 1854.877500, max = 4196.500000)
print(df['receita_total'].describe())
condicoes = [
    df['receita_total'] < 440.762500,
    (df['receita_total'] >= 440.762500) & (df['receita_total'] < 1854.877500),
    df['receita_total'] >= 1854.877500
]
faixas = ['Baixo Valor', 'Medio Valor', 'Alto Valor']
df['faixa_receita_item'] = "Nao Classificado"

for condicao, faixa in zip(condicoes, faixas):
    df.loc[condicao, "faixa_receita_item"] = faixa

# VERIFICACAO
print("")
print("=== VERIFICACAO: NOVAS COLUNAS ===")
novas_colunas = ['receita_total', 'mes', 'mes_nome', 'trimestre', 'ano', 'faixa_receita_item']
print(f"\nTipos de dados\n{df[novas_colunas].dtypes}")
print(f"\nNulos\n{df[novas_colunas].isnull().sum()}")
print(f"\nDados unicos: mes\n{df["mes_nome"].unique()}")
print(f"\nDados unicos: trimestre\n{df["trimestre"].unique()}")
print(f"\nDados unicos: faixa_receita_item\n{df["faixa_receita_item"].value_counts()}")
print(f"\nAmostra do DF\n{df[novas_colunas].head()}")