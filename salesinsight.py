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