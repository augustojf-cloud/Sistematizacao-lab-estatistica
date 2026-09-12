"""
========================================================================
 SISTEMATIZAÇÃO - Laboratório de Estatística em Python
 Módulo 0: Carregamento e Inspeção do Dataset (versão interativa)
========================================================================

Versão Streamlit do Módulo 0: mesma lógica de carregamento/inspeção
que já estava em "Modulo 0/modulo0_dataset - rodando.py", só que
mostrando o resultado numa interface web em vez de no console.
"""

import os
import sys

# Permite importar montecarlo.py e statslocal.py, que ficam na pasta
# raiz do projeto (um nivel acima de "Modulo 0/", onde este
# arquivo esta agora).
_PASTA_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_MODULO1 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 1")
_PASTA_MODULO2 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 2")
_PASTA_MODULO3 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 3")
_PASTA_MODULO4 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 4")
_PASTA_MODULO5 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 5")
for _pasta in (_PASTA_RAIZ_PROJETO, _PASTA_MODULO1, _PASTA_MODULO2, _PASTA_MODULO3, _PASTA_MODULO4, _PASTA_MODULO5):
    if _pasta not in sys.path:
        sys.path.insert(0, _pasta)

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import sys
sys.path.append("../Modulo 5")  


import montecarlo as mc
from statslocal import media
from modulo2_estatistica_interativa import modulo2_estatistica_interativa
from modulo4_distribuicoes_teoricas import modulo4_distribuicoes_teoricas
from regressao import render_modulo5

NOME_ABA = "Sheet1"
SEPARADOR = ";"
CODIFICACAO = "latin1"

# app.py agora mora dentro da pasta "Modulo 0/", junto com o dataset
PASTA_DADOS = ""
ARQUIVOS_LOCAIS_PADRAO = ["SISDEPEN.xlsx", "SISDEPEN.xls", "SISDEPEN.csv"]


def carregar_dataset(origem, nome_arquivo, separador=SEPARADOR, codificacao=CODIFICACAO, aba=NOME_ABA):
    extensao = nome_arquivo.lower().split(".")[-1]
    try:
        if extensao in ("xlsx", "xls"):
            df = pd.read_excel(origem, sheet_name=aba)
        elif extensao == "csv":
            df = pd.read_csv(origem, sep=separador, encoding=codificacao)
        else:
            st.error(f"Formato de arquivo não suportado: .{extensao}")
            return None
        return df
    except UnicodeDecodeError:
        st.error(
            "Erro de codificação ao ler o arquivo. "
            f"Tentei usar a codificação '{codificacao}', mas não funcionou para este arquivo."
        )
        return None
    except ImportError:
        st.error(
            "Falta uma biblioteca para ler este tipo de arquivo. "
            "Verifique se 'openpyxl' está instalado (necessário para arquivos .xlsx)."
        )
        return None
    except Exception as erro:
        st.error(f"Não foi possível carregar o arquivo: {erro}")
        return None


def inspecionar_dataset(df):
    st.subheader("4.1 Primeiras linhas do dataset")
    st.dataframe(df.head())

    st.subheader("4.2 Dimensão do dataset")
    col1, col2, col3 = st.columns(3)
    col1.metric("Linhas", df.shape[0])
    col2.metric("Colunas", df.shape[1])
    col3.metric("Linhas duplicadas", int(df.duplicated().sum()))

    st.subheader("4.3 Nome de todas as colunas")
    st.write(list(df.columns))

    st.subheader("4.4 Tipos de dado de cada coluna")
    st.dataframe(df.dtypes.astype(str).rename("tipo"))

    st.subheader("4.5 Estatísticas descritivas (pandas.describe)")
    st.caption(
        "Referência de conferência (usa pandas). As estatísticas calculadas "
        "'na unha', sem bibliotecas prontas, ficam no Módulo 1 (src/statslocal.py)."
    )
    st.dataframe(df.describe())

    st.subheader("4.6 Valores ausentes (células vazias) por coluna")
    ausentes = df.isnull().sum()
    ausentes = ausentes[ausentes > 0].sort_values(ascending=False)
    if len(ausentes) == 0:
        st.success("Nenhum valor ausente encontrado.")
    else:
        st.dataframe(ausentes.rename("qtd_ausentes"))


def modulo3_monte_carlo(df):
    st.header("Módulo 3 — Probabilidade e Simulação (Monte Carlo)")
    st.markdown(
        "Demonstração prática de dois resultados fundamentais da estatística, "
        "usando sorteios aleatórios (com reposição) sobre uma coluna numérica "
        "real do SISDEPEN."
    )

    colunas_numericas = df.select_dtypes(include="number").columns.tolist()
    if len(colunas_numericas) == 0:
        st.warning("Não há colunas numéricas no dataset para simular.")
        return

    coluna = st.selectbox("Coluna numérica a usar como população", colunas_numericas)
    populacao = df[coluna].dropna().tolist()

    if len(populacao) < 2:
        st.warning("Essa coluna não tem dados suficientes para simular.")
        return

    media_real = media(populacao)
    st.metric(f"Média real de '{coluna}' (população completa, n={len(populacao)})", f"{media_real:.4f}")

    semente = st.number_input(
        "Semente aleatória (mesma semente = mesmo resultado, útil para reproduzir)",
        min_value=0, value=42, step=1,
    )

    # ------------------------------------------------------------------
    # Lei dos Grandes Números
    # ------------------------------------------------------------------
    st.subheader("3.1 Lei dos Grandes Números")
    st.caption(
        "Conforme aumentamos o número de sorteios, a média acumulada dos "
        "valores sorteados converge para a média real da população (linha "
        "tracejada vermelha)."
    )
    n_sorteios = st.slider("Número de sorteios", min_value=10, max_value=5000, value=1000, step=10)

    medias_acumuladas = mc.lei_dos_grandes_numeros(populacao, n_sorteios, semente=int(semente))

    fig1, ax1 = plt.subplots()
    ax1.plot(range(1, n_sorteios + 1), medias_acumuladas, linewidth=1)
    ax1.axhline(media_real, color="red", linestyle="--", label=f"Média real = {media_real:.2f}")
    ax1.set_xlabel("Número de sorteios")
    ax1.set_ylabel("Média acumulada")
    ax1.set_title("Lei dos Grandes Números")
    ax1.legend()
    st.pyplot(fig1)

    # ------------------------------------------------------------------
    # Teorema Central do Limite
    # ------------------------------------------------------------------
    st.subheader("3.2 Teorema Central do Limite")
    st.caption(
        "Sorteamos várias amostras (todas do mesmo tamanho) e calculamos a "
        "média de cada uma. O histograma dessas médias tende a um formato "
        "de sino (distribuição normal), mesmo que a coluna original não "
        "tenha esse formato."
    )
    col_a, col_b = st.columns(2)
    tamanho_amostra = col_a.slider("Tamanho de cada amostra", min_value=2, max_value=200, value=30, step=1)
    n_simulacoes = col_b.slider("Número de amostras simuladas", min_value=100, max_value=5000, value=1000, step=100)

    medias_das_amostras = mc.teorema_central_limite(
        populacao, tamanho_amostra, n_simulacoes, semente=int(semente)
    )

    fig2, ax2 = plt.subplots()
    ax2.hist(medias_das_amostras, bins=40, edgecolor="black")
    ax2.axvline(media_real, color="red", linestyle="--", label=f"Média real = {media_real:.2f}")
    ax2.set_xlabel("Média da amostra")
    ax2.set_ylabel("Frequência")
    ax2.set_title(f"Distribuição das médias amostrais (n={tamanho_amostra} por amostra)")
    ax2.legend()
    st.pyplot(fig2)


def main():
    st.set_page_config(page_title="SISTEMATIZAÇÃO - Laboratório de Estatística", layout="wide")
    st.title("SISTEMATIZAÇÃO — Laboratório de Estatística em Python")
    st.caption("Dataset: SISDEPEN (Sistema de Informações do Departamento Penitenciário Nacional)")
    st.header("Módulo 0 — Carregamento e Inspeção do Dataset")

    pasta_script = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(pasta_script, PASTA_DADOS)

    caminho_local = None
    for nome in ARQUIVOS_LOCAIS_PADRAO:
        candidato = os.path.join(pasta_dados, nome)
        if os.path.exists(candidato):
            caminho_local = candidato
            break

    df = None
    if caminho_local is not None:
        st.success(f"Dataset local encontrado: {os.path.basename(caminho_local)}")
        df = carregar_dataset(caminho_local, os.path.basename(caminho_local))

    arquivo_enviado = st.file_uploader(
        "Ou envie um arquivo (.xlsx, .xls ou .csv)", type=["xlsx", "xls", "csv"]
    )
    if arquivo_enviado is not None:
        df = carregar_dataset(arquivo_enviado, arquivo_enviado.name)

    if df is not None:
        inspecionar_dataset(df)
        st.divider()
        modulo2_estatistica_interativa(df)
        st.divider()
        modulo3_monte_carlo(df)
        st.divider()
        modulo4_distribuicoes_teoricas(df)
        st.divider()
        render_modulo5(df)
    else:
        st.warning(
            "Nenhum dataset carregado ainda. Verifique se o arquivo SISDEPEN está na mesma "
            "pasta deste app.py (Modulo 0/), ou envie um arquivo pelo campo acima."
        )


if __name__ == "__main__":
    main()
