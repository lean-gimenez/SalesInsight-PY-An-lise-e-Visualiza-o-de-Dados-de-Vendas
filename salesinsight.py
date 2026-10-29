# Importar librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

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
COL_FAIXA_DESCONTO = 'faixa_desconto'


# ===========================================
# === CARREGAR DATASET E TRANSFORMAR A DF ===
# ===========================================

nome_dataset = "vendas.csv"

def carregar_dados(nome_dataset):
    # Transformar dataset a dataframe
    df_bruto = pd.read_csv(nome_dataset)
    return df_bruto


# ===========================================
# ======== INSPECAO INICIAL DE DADOS ========
# ===========================================

def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""

    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"\nShape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")


# ===========================================
# ============ LIMPEZA DE DADOS =============
# ===========================================

def tratar_dados(df):
    """
    Trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, convertidas e finais.
    """

    # Para nao modificar o df bruto
    df = df.copy()

    print("\n=== LIMPEZA DE DADOS ===")

    # ESTADO INICIAL
    linhas_inicio = len(df)

    # LIMPEZA
    # 1. Remover espacos extras nas colunas de texto e converter possiveis valores vazios ("") em NaN
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].str.strip()
    df = df.replace("", np.nan)

    # 2. Converter datas e descartar invalidas
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], format='%m/%d/%Y', errors='coerce')
    # Ver as datas convertidas antes de fazer metodo dropna
    convertidas = df[COL_DATA].notna().sum()
    datas_invalidas = df[COL_DATA].isna().sum()
    df = df.dropna(subset=[COL_DATA])

    # 3. Remover duplicados
    df = df.drop_duplicates()
    duplicados_removidos = linhas_inicio - len(df)

    # 4. Garantir que quantidade seja int e preco_unidade seja float
    df[COL_QUANTIDADE] = df[COL_QUANTIDADE].astype(int)
    df[COL_PRECO_UNIDADE] = df[COL_PRECO_UNIDADE].astype(float)

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


# ===========================================
# ============ COLUNAS DERIVADAS ============
# ===========================================

def criar_colunas(df): 
    # Copiar o df_limpo num df novo
    df = df.copy()

    # Criacao de colunas derivadas
    # Receita total
    df[COL_RECEITA] = df[COL_QUANTIDADE] * df[COL_PRECO_UNIDADE] * (1 - df[COL_DESCONTO])
    df[COL_RECEITA] = df[COL_RECEITA].round(2)

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
    print()
    print("=== NOVO DATAFRAME ===")
    print()
    print(f"DF com {df.shape[0]} linhas e {df.shape[1]} colunas.")
    print()
    print(f"Colunas: {list(df.columns)}")

    return df


# ===========================================
# ============= METRICAS DO DF ==============
# ===========================================

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
    top_categorias = receita_categorias.sort_values(by=COL_RECEITA, ascending=False).head(5)

    # Receita total e ticket médio por região.
    receita_regiao = df.groupby(COL_REGIAO).agg(
        receita_total=(COL_RECEITA, 'sum'),
        ticket_medio=(COL_RECEITA, 'mean')
    ).reset_index()
    receita_regiao['ticket_medio'] = receita_regiao['ticket_medio'].round(2)

    # Quantidade de vendas com DESCONTO por METODO DE PAGO
    com_desconto = df[df[COL_DESCONTO] > 0].copy()
    com_desconto[COL_FAIXA_DESCONTO] = df[COL_DESCONTO].apply(
        lambda x: '<10%' if x < 0.1 else ('10-20%' if x <= 0.2 else '>20%')
    )

    ordem_descontos = ['<10%', '10-20%', '>20%']

    com_desconto[COL_FAIXA_DESCONTO] = pd.Categorical(
        com_desconto[COL_FAIXA_DESCONTO], categories=ordem_descontos, ordered=True
    )

    tabela_descontos = (
        com_desconto
        .groupby([COL_PAGAMENTO, COL_FAIXA_DESCONTO], observed=True)
        .size()
        .reset_index(name='quantidade_vendas')
    )

    metricas = {
        "por_mes": resumo_mensal,
        "top_categorias": top_categorias,
        "por_regiao": receita_regiao,
        "desconto_por_pagamento": tabela_descontos,
    }

    return metricas


def resumo(dict):
    for titulo, tabela in dict.items():
        print(f"\n=== {titulo} ===")
        print(tabela.to_string(index=False))


# ===========================================
# ========= SEGMENTACAO DE CLIENTES =========
# ===========================================

def processar_coluna(df, coluna, funcao_transformadora, nova_coluna=None):
   """Processa coluna do df e cria uma nova"""

   df = df.copy()
   nova_coluna = nova_coluna or f"{coluna}_transformada"
   df[nova_coluna] = df[coluna].apply(funcao_transformadora)

   return df


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
        .round(2)
        .reset_index()
        .rename(columns={COL_CLIENTE:'cliente', COL_RECEITA:'total_gasto'})
    )

    # Quartis 1 e 3 da coluna total_gasto para calcular segmentos
    q1 = clientes['total_gasto'].quantile(0.25)
    q3 = clientes['total_gasto'].quantile(0.75)

    clientes = processar_coluna(
        clientes, 'total_gasto',
        lambda x: 'Bronze' if x < q1 else ('Prata' if x <= q3 else 'Ouro'),
        nova_coluna='segmento'
    )

    return clientes

def exibir_segmentacao(clientes):
    """Exibe top 10 clientes e distribuicao por segmento"""

    # Top 10 clientes
    print("\nTOP 10 CLIENTES")
    top10_clientes = clientes.sort_values(by='total_gasto', ascending=False).head(10)
    print(top10_clientes.to_string(index=False))

    # Distribuicao por segmento
    resumo_segmento = clientes.groupby('segmento').agg(
        n_clientes=('cliente', 'count'),
        total_gasto=('total_gasto', lambda x: x.sum().round(2)),
    )
    resumo_segmento['%_clientes'] = (resumo_segmento['n_clientes'] / resumo_segmento['n_clientes'].sum() * 100).round(2)
    resumo_segmento['%_gasto'] = (resumo_segmento['total_gasto'] / resumo_segmento['total_gasto'].sum() * 100).round(2)

    ordem = ['Bronze', 'Prata', 'Ouro']

    print("\nDISTRIBUICAO POR SEGMENTO")
    print(clientes['segmento'].value_counts().reindex(ordem))
    print()
    print(resumo_segmento.reindex(ordem))


# ===========================================
# ========= VISUALIZAÇÃO DOS DADOS ==========
# ===========================================

# Criação de
# Grafico de LINHAS: receita_por_mes
# Grafico de BARRAS: top_categorias
# Grafico de DISPERÇÃO: quantidade_vs_receita
# Grafico 2x2 painel_resumo com graficos anteriores + receita por regiao (G de BARRAS)
# EXTRAS
# Grafico de BARRAS: receita_por_trimestre """Mostrar a evolucao da receita acumulada por trimestre (Q1 a Q4) para ver estacionalidade."""
# Grafico HEATMAP: matriz_correlacao_trimestral """Visualizar estacionalidade comparando anos contra trimestres para identificar patrones de concentración de ventas."""
# Grafico de PIZZA: distribuicao_segmentos """Mostrar a participacao porcentual que tem cada segmento de clientes."""
# Grafico HISTOGRAMA: vendas_por_faixa_preco """Mostrar volumen de vendas de cada rango (BAIXO, MEDIO, ALTO)."
# Grafico de LINHAS: tendencia_projecao """Graficar a evolucao mensal da receita junto com a estimacao da media para os próximos meses."

# configuracao visual global
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["legend.fontsize"] = 11
PALETA = ["#0a3f8a", "#95101b", "#0b8741", "#bbb807"]


# --- Gaurdar figura
def guardar_figura(fig, nome_arquivo, mostrar=False):
    """Ajusta o layout, salva a figura em PNG e a fecha."""

    # Criar pasta para guardar os graficos
    pasta_graficos = "outputs/graficos"
    os.makedirs(pasta_graficos, exist_ok=True)
    
    # ajustar tamanho da figura
    plt.tight_layout()
    
    # guardar grafico 
    plt.savefig(os.path.join(pasta_graficos, nome_arquivo), dpi=150)

    # mostrar grafico depois de salvar e antes de fechar
    if mostrar:
        plt.show()
    
    # fechar grafico
    plt.close(fig)


# --- Grafico de LINHAS: receita_por_mes
def grafico_receita_por_mes(ax, metricas):
    """Desenha a linha de receita por mes no eixo recebido."""

    # Trazer tabela de receita por mes
    por_mes = metricas['por_mes']

    # Grafico de linhas
    ax.plot(por_mes[COL_MES], por_mes[COL_RECEITA], marker="o", linewidth=2)
    ax.set_title("Receita Total por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita Total ($)")


# --- Grafico de BARRAS: top_categorias
def grafico_top_categorias(ax, metricas):
    """Desenha as barras de receita por categoria no eixo recebido."""

    # Trazer tabela de receita por mes
    top_categorias = metricas['top_categorias']

    # Grafico de barras
    sns.barplot(
        data=top_categorias, y=COL_CATEGORIA, x=COL_RECEITA,
        hue=COL_CATEGORIA, legend=False, palette=PALETA, ax=ax
        )
    ax.set_title("Top Categorias")
    ax.set_xlabel("Categorias")
    ax.set_ylabel("Receita")


# --- Grafico de DISPERÇÃO: quantidade_vs_receita
def grafico_quantidade_vs_receita(ax, df):
    """Desenha a dispersao quantidade x receita, colorida por categoria."""

    # Grafico de dispercao
    df = df.sample(800, random_state=42)
    rng = np.random.default_rng(42) # Jitter para ver melhor a dispercao
    x_jitter = df[COL_QUANTIDADE] + rng.uniform(-0.25, 0.25, len(df)) # maior largo das colunas

    sns.scatterplot(
        data=df, x=x_jitter, y=COL_RECEITA,
        hue=COL_CATEGORIA, palette=PALETA, alpha=0.5, ax=ax
        )
    ax.set_title("Quantidade vs Receita")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Receita Total")
    ax.legend(title="Categoria")


# --- Grafico de BARRAS: receita_por_regiao
def grafico_receita_por_regiao(ax, metricas):
    """Desenha as barras de receita por regiao no eixo recebido."""

    regiao = metricas['por_regiao']
    
    # Grafico de barras
    sns.barplot(
        data=regiao, y=COL_REGIAO, x=COL_RECEITA,
        hue=COL_REGIAO, legend=False, palette=PALETA, ax=ax
        )
    ax.set_title("Receita por região")
    ax.set_xlabel("Receita Total")
    ax.set_ylabel("Região")


# Grafico 2x2 painel_resumo com graficos anteriores
def grafico_painel_resumo(df, metricas, mostrar=False):
    """Gera a figura 2x2 reutilizando as funcoes de desenho."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    grafico_receita_por_mes(axes[0, 0], metricas) # linha
    grafico_top_categorias(axes[0, 1], metricas) # barras
    grafico_quantidade_vs_receita(axes[1, 0], df) # dispersao
    grafico_receita_por_regiao(axes[1, 1], metricas) # receita por regiao

    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)

    nome_arquivo = "painel_resumo.png"
    guardar_figura(fig, nome_arquivo, mostrar=mostrar)


# --- EXTRAS
# Grafico de BARRAS: receita_por_trimestre 
def grafico_receita_por_trimestre(ax, df):
    """Mostrar a evolucao da receita acumulada por trimestre (Q1 a Q4) para ver estacionalidade."""
    df = df.copy()

    # Trazer tabela de receita por trimestre
    receita_trimestre = df.groupby(COL_TRIMESTRE)[COL_RECEITA].sum().reset_index()

    # Grafico de barras
    sns.barplot(
        data=receita_trimestre, y=COL_RECEITA, x=COL_TRIMESTRE,
        legend=False, ax=ax
        )
    ax.set_title("Estacionalidade: Receita por trimestre")
    ax.set_xlabel("Trimestre")
    ax.set_ylabel("Receita")
    

# Grafico HEATMAP: matriz_correlacao_trimestral
def grafico_matriz_correlacao_trimestral(ax, df):
    """Visualizar estacionalidade comparando anos contra trimestres para identificar patrones de concentración de ventas."""
    df = df.copy()

    df_pivot = df.groupby([COL_ANO, COL_TRIMESTRE])[COL_RECEITA].sum().unstack(level=COL_TRIMESTRE)
    sns.heatmap(data=df_pivot, cmap='YlGnBu', annot=True, 
                linecolor='white', fmt=',.0f', annot_kws={'size': 7},
                cbar_kws={'label': 'Receita Total'}, ax=ax)
    ax.set_title('Correlação de Receita por Ano e Trimestre')
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Ano')


# Grafico de PIZZA: distribuicao_segmentos
def grafico_distribuicao_segmentos(ax, df):
    """Mostrar a participacao porcentual que tem cada segmento de clientes."""
    df = df.copy()

    df_clientes = segmentar_clientes(df)
    segmentos = df_clientes['segmento'].value_counts()
    ax.pie(x=segmentos, labels=segmentos.index, colors=PALETA[0:3], autopct='%1.1f%%')
    ax.set_title('Distribuição de Clientes por Segmento')


# Grafico HISTOGRAMA: vendas_por_faixa_preco
def grafico_vendas_por_faixa_preco(ax, df):
    """Mostrar volumen de vendas de cada rango (BAIXO, MEDIO, ALTO)."""
    df = df.copy()

    n_anos = df[COL_ANO].nunique()

    sns.histplot(
        data=df, x=COL_ANO, hue=COL_FAIXA,
        weights=COL_RECEITA, multiple='stack',
        palette=PALETA[0:3], shrink=0.9, bins=n_anos, ax=ax
    )
    ax.set_title('Receita por Ano e Faixa de Preço')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Receita Total')
    ax.set_xticks(sorted(df[COL_ANO].unique()))
    ax.tick_params(axis='x', rotation=45)


# Grafico 2x2 painel_resumo_extra com graficos anteriores
def grafico_painel_resumo_extra(df, mostrar=False):
    """Gera a figura 2x2 reutilizando as funcoes de desenho."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    grafico_receita_por_trimestre(axes[0, 0], df) # linha
    grafico_matriz_correlacao_trimestral(axes[0, 1], df) # barras
    grafico_distribuicao_segmentos(axes[1, 0], df) # dispersao
    grafico_vendas_por_faixa_preco(axes[1, 1], df) # receita por regiao

    fig.suptitle("SalesInsight PY - Painel Resumo Extra", fontsize=16)

    nome_arquivo = "painel_resumo_extra.png"
    guardar_figura(fig, nome_arquivo, mostrar=mostrar)


# --- Gerar e guardar os graficos
def gerar_graficos(df, metricas):
    """Gera e salva as figuras"""
    
    # Linhas: receita por mes
    fig, ax = plt.subplots()
    grafico_receita_por_mes(ax, metricas)
    guardar_figura(fig, "receita_por_mes.png")

    # Barras: top categorias
    fig, ax = plt.subplots()
    grafico_top_categorias(ax, metricas)
    guardar_figura(fig, "top_categorias.png")

    # Dispercao: quantidade vs receita
    fig, ax = plt.subplots()
    grafico_quantidade_vs_receita(ax, df)
    guardar_figura(fig, "quantidade_vs_receita.png")

    # Barras: receita por regiao
    fig, ax = plt.subplots()
    grafico_receita_por_regiao(ax, metricas)
    guardar_figura(fig, "receita_por_regiao.png")

    # Painel resumo
    respuesta = input("\nDeseja ver o painel resumo com os graficos? S/N: ")
    mostrar = respuesta.strip().upper() == "S"
    grafico_painel_resumo(df, metricas, mostrar=mostrar)

    # Barras: receita_por_trimestre
    fig, ax = plt.subplots()
    grafico_receita_por_trimestre(ax, df)
    guardar_figura(fig, "receita_por_trimestre")

    # Heatmap: matriz_correlacao_trimestral
    fig, ax = plt.subplots()
    grafico_matriz_correlacao_trimestral(ax, df)
    guardar_figura(fig, "matriz_correlacao_trimestral")

    # Pizza: distribuicao_segmentos
    fig, ax = plt.subplots()
    grafico_distribuicao_segmentos(ax, df)
    guardar_figura(fig, "distribuicao_segmentos")

    # Histograma: vendas_por_faixa_preco
    fig, ax = plt.subplots()
    grafico_vendas_por_faixa_preco(ax, df)
    guardar_figura(fig, "vendas_por_faixa_preco")

    # painel_resumo_extra
    respuesta = input("Deseja ver mais graficos? S/N: ")
    mostrar = respuesta.strip().upper() == "S"
    grafico_painel_resumo_extra(df, mostrar=mostrar)




# ===========================================
# ======== EXPORTAÇÃO DE RESULTADOS =========
# ===========================================

# --- Definir estatisticas
def calcular_estatisticas(df):
    """Calcula estatisticas gerais do df e retorna um dict"""
    return {
        'total_faturamento': df[COL_RECEITA].sum(),
        'total_vendas': len(df),
        'ticket_medio': df[COL_RECEITA].mean(),
        'desconto_medio': df[COL_DESCONTO].mean(),
        }


def exportar_resultados(metricas, clientes, estatisticas):
    """Exporta os resultados do projeto em CSV e JSON."""

    # Criar pasta outputs
    os.makedirs("outputs", exist_ok=True)

    # Guardar df "por_mes" do dict metricas como csv
    metricas["por_mes"].to_csv("outputs/metricas_por_mes.csv",
                               index=False, encoding="utf-8-sig")

    # Guardar df clientes (segmentados) como csv
    clientes.to_csv("outputs/segmentacao_clientes.csv",
                    index=False, encoding="utf-8-sig")

    # Modificar dados para ser lidos por json (dictionary comprehension)
    serializavel = {key: round(float(value), 2)
                    for key, value in estatisticas.items()}
    # Rota para guardar arquivo json
    caminho = "outputs/estatisticas_gerais.json"
    # Criar/guardar json (write)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(serializavel, f, indent=4, ensure_ascii=False)

    # Leitura de volta para confirmar a escrita (read)
    with open(caminho, "r", encoding="utf-8") as f:
        conferencia = json.load(f) # Leitura fechada, mas dados guardados na variável conferencia
    # Confirmar guardado e mostrar JSON
    print(f"\nJSON gravado e lido: \n{conferencia}")


# ===========================================
# ============ CLASSE ANALISADOR ============
# ===========================================

# --- Definir classe analisador
class Analisador:
    """Executa todas as funcoes para analisar as vendas"""

    def __init__(self):
        self.df_bruto = None # é df
        self.df_limpo = None # é df
        self.df = None # é df
        self.relatorio = {} # é dict
        self.metricas = {} # é dict
        self.clientes = None # é df
        self.estatisticas = {} # é dict


    def carregar(self, dataset):
        """Carrega os dados do dataset e converte a df"""
        self.df_bruto = carregar_dados(dataset)


    def inspecionar(self):
        """Exibe a inspecao inicial do df bruto"""
        inspecionar_dados(self.df_bruto)


    def transformar(self):
        """Limpa os dados e cria as colunas derivadas"""
        self.df_limpo, self.relatorio = tratar_dados(self.df_bruto)

        print("\n=== RELATÓRIO DE LIMPEZA ===")
        print()
        for key, value in self.relatorio.items():
            print(f"{key}: {value}")

        self.df = criar_colunas(self.df_limpo)


    def analisar(self):
        """Calcula metricas, segmentacao de clientes e estatisticas"""
        self.metricas = calcular_metricas(self.df)
        self.clientes = segmentar_clientes(self.df)
        self.estatisticas = calcular_estatisticas(self.df)

    
    def resumir(self):
        """Exibe as metricas e a segmentacao de clientes"""
<<<<<<< HEAD
        print("\n=== RESUMO DE METRICAS ===")
=======
        print()
        print("=== RESUMO DE METRICAS ===")
>>>>>>> develop
        resumo(self.metricas)
        exibir_segmentacao(self.clientes)


    def visualizar(self):
        """Gera, guarda e mostra os graficos"""
        gerar_graficos(self.df, self.metricas)
    

    def exportar(self):
        """Exporta resultados em formato csv e jason e mostra o json na consola"""
        exportar_resultados(self.metricas, self.clientes, self.estatisticas)


# ===========================================
# == FUNÇAO MAIN QUE REUNE TODAS AS FUNÇÕES =
# ===========================================

def main():
    analisador = Analisador()
    analisador.carregar(nome_dataset)
    analisador.inspecionar()
    analisador.transformar()
    analisador.analisar()
    analisador.resumir()
    analisador.visualizar()
    analisador.exportar()


if __name__ == "__main__":
    main()