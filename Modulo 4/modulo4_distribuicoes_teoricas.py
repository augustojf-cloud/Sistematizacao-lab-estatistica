"""
========================================================================
 SISTEMATIZAÇÃO - Laboratório de Estatística em Python
 Módulo 4: Distribuições Teóricas
========================================================================

Objetivo (conforme o README que existia nesta pasta antes deste
arquivo): sobrepor uma curva de distribuição teórica ao histograma dos
dados reais de uma coluna numérica do SISDEPEN, para comparar a
distribuição observada com a esperada.

O usuário escolhe, na tela, uma coluna numérica e uma entre três
distribuições teóricas para sobrepor ao histograma:

- Normal (Gaussiana): parâmetros = média e desvio padrão da própria
  coluna (calculados pelo Módulo 1 -- statslocal.py).
- Uniforme contínua: parâmetros = mínimo e máximo observados na coluna.
- Exponencial: parâmetro de taxa (lambda) = 1 / média da coluna.

As densidades de probabilidade (densidade_normal, densidade_uniforme,
densidade_exponencial) são calculadas "na unha" no Módulo 1
(statslocal.py), pelas fórmulas fechadas de cada distribuição -- não
usamos scipy.stats para isso. O histograma é feito com matplotlib
(plotagem/binning, não é uma função estatística pronta), com
density=True para que a área das barras fique na mesma escala da
curva teórica (ambas somam área 1), permitindo a comparação visual.
"""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- Importa o núcleo estatístico próprio (Módulo 1) ---
_PASTA_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_MODULO1 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 1")
if _PASTA_MODULO1 not in sys.path:
    sys.path.insert(0, _PASTA_MODULO1)
from statslocal import (
    media,
    desvio_padrao,
    densidade_normal,
    densidade_uniforme,
    densidade_exponencial,
)

DISTRIBUICOES = ("Normal", "Uniforme", "Exponencial")


def _pontos_uniformes(inicio: float, fim: float, quantidade: int):
    """
    Gera 'quantidade' pontos igualmente espaçados entre inicio e fim
    (equivalente a numpy.linspace, feito na mão para não depender do
    numpy aqui).
    """
    if quantidade < 2 or fim <= inicio:
        return [inicio]
    passo = (fim - inicio) / (quantidade - 1)
    return [inicio + i * passo for i in range(quantidade)]


def _curva_teorica(pontos_x, dados, distribuicao: str):
    """
    Calcula a curva teórica (lista de densidades, uma por ponto de
    pontos_x) para a distribuição escolhida, estimando os parâmetros a
    partir dos próprios dados. Retorna (pontos_y, parametros), onde
    parametros é um dict com os valores estimados para exibir na tela.
    """
    if distribuicao == "Normal":
        m = media(dados)
        dp = desvio_padrao(dados, amostral=True)
        pontos_y = [densidade_normal(x, m, dp) for x in pontos_x]
        parametros = {"média": m, "desvio padrão": dp}
    elif distribuicao == "Uniforme":
        minimo, maximo = min(dados), max(dados)
        pontos_y = [densidade_uniforme(x, minimo, maximo) for x in pontos_x]
        parametros = {"mínimo": minimo, "máximo": maximo}
    elif distribuicao == "Exponencial":
        m = media(dados)
        taxa = 1.0 / m if m != 0 else 0.0
        pontos_y = [densidade_exponencial(x, taxa) for x in pontos_x]
        parametros = {"taxa (λ)": taxa, "média (1/λ)": m}
    else:
        raise ValueError(f"Distribuição desconhecida: {distribuicao}")

    return pontos_y, parametros


def plotar_histograma_com_curva(dados, distribuicao: str, bins: int = 30):
    """
    Desenha o histograma normalizado (density=True) dos dados reais e
    sobrepõe a curva de densidade teórica escolhida.

    Retorna (fig, parametros): a figura do matplotlib e um dict com os
    parâmetros estimados da distribuição (para exibir na tela).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(
        dados, bins=bins, density=True, edgecolor="black",
        alpha=0.6, label="Dados reais (histograma)",
    )

    minimo, maximo = min(dados), max(dados)
    margem = (maximo - minimo) * 0.05 if maximo > minimo else 1.0
    pontos_x = _pontos_uniformes(minimo - margem, maximo + margem, 300)
    pontos_y, parametros = _curva_teorica(pontos_x, dados, distribuicao)

    ax.plot(pontos_x, pontos_y, color="red", linewidth=2, label=f"Curva teórica ({distribuicao})")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidade")
    ax.set_title(f"Histograma dos dados reais vs. distribuição {distribuicao} teórica")
    ax.legend()
    fig.tight_layout()

    return fig, parametros


def modulo4_distribuicoes_teoricas(df: pd.DataFrame) -> None:
    """Ponto de entrada do Módulo 4 -- chamado a partir do app.py (Módulo 0)."""
    st.header("Módulo 4 — Distribuições Teóricas")
    st.markdown(
        "Escolha uma coluna numérica e uma distribuição teórica para "
        "sobrepor ao histograma dos dados reais. Quanto mais a curva "
        "vermelha acompanhar o formato das barras do histograma, mais "
        "a coluna se aproxima daquela distribuição teórica."
    )

    colunas_numericas = df.select_dtypes(include="number").columns.tolist()
    if not colunas_numericas:
        st.warning("Não há colunas numéricas no dataset para analisar.")
        return

    col1, col2 = st.columns(2)
    with col1:
        coluna = st.selectbox("Coluna numérica", colunas_numericas, key="m4_coluna")
    with col2:
        distribuicao = st.selectbox("Distribuição teórica", DISTRIBUICOES, key="m4_distribuicao")

    dados = df[coluna].dropna().tolist()
    if distribuicao == "Exponencial":
        # A densidade exponencial só é definida para x >= 0.
        removidos = len(dados)
        dados = [x for x in dados if x >= 0]
        removidos -= len(dados)
        if removidos:
            st.caption(f"{removidos} valor(es) negativo(s) removido(s) (Exponencial só é definida para x ≥ 0).")

    if len(dados) < 5:
        st.info("Poucos dados válidos nessa coluna para essa distribuição.")
        return

    bins = st.slider(
        "Número de faixas (bins) do histograma",
        min_value=5, max_value=100, value=30, step=5, key="m4_bins",
    )

    try:
        fig, parametros = plotar_histograma_com_curva(dados, distribuicao, bins=bins)
    except ValueError as erro:
        st.warning(f"Não foi possível calcular a curva teórica: {erro}")
        return

    try:
        st.pyplot(fig)
    finally:
        plt.close(fig)

    st.caption("Parâmetros estimados a partir dos dados reais (Módulo 1 — statslocal.py):")
    cols = st.columns(len(parametros))
    for coluna_metric, (nome, valor) in zip(cols, parametros.items()):
        coluna_metric.metric(nome, f"{valor:.4f}")
