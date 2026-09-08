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

import pandas as pd
import streamlit as st

NOME_ABA = "Sheet1"
SEPARADOR = ";"
CODIFICACAO = "latin1"

# O dataset já está commitado no repositório, dentro da pasta "Modulo 0/"
PASTA_DADOS = "Modulo 0"
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
        st.success(f"Dataset local encontrado: {PASTA_DADOS}/{os.path.basename(caminho_local)}")
        df = carregar_dataset(caminho_local, os.path.basename(caminho_local))

    arquivo_enviado = st.file_uploader(
        "Ou envie um arquivo (.xlsx, .xls ou .csv)", type=["xlsx", "xls", "csv"]
    )
    if arquivo_enviado is not None:
        df = carregar_dataset(arquivo_enviado, arquivo_enviado.name)

    if df is not None:
        inspecionar_dataset(df)
    else:
        st.warning(
            f"Nenhum dataset carregado ainda. Verifique se o arquivo SISDEPEN está dentro "
            f"da pasta '{PASTA_DADOS}/', ou envie um arquivo pelo campo acima."
        )


if __name__ == "__main__":
    main()
