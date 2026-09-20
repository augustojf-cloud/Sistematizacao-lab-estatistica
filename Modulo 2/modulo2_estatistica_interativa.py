"""
========================================================================
 SISTEMATIZAÇÃO - Laboratório de Estatística em Python
 Módulo 2: Estatística Descritiva Interativa
========================================================================

Versão corrigida a partir da proposta do Matheus (modulo2_graficos_otimizado.py),
integrada ao núcleo estatístico próprio do Módulo 1 (statslocal.py) e à
interface do Streamlit (Módulo 0).

O que este módulo entrega, conforme pedido na sistematização:
1. Gráficos interativos: visão macro por categoria + detalhe por
   subcategoria (mantido da proposta original do Matheus, com dropdowns
   pra escolher as colunas direto na tela)
2. Tabela de frequências de uma coluna categórica escolhida pelo usuário
3. Detecção de outliers via IQR — usando quartis()/iqr() do Módulo 1,
   não uma função pronta de biblioteca (numpy/pandas/scipy)

Ajustes feitos em relação ao arquivo original enviado pelo Matheus:
- PASTA_GRAFICOS agora aponta sempre para a pasta "graficos/" da raiz
  do projeto (a mesma que analise_completa.py já usa e onde já estão os
  ~50 PNGs gerados), em vez de uma pasta nova dentro de "Modulo 2/".
- Tabela de frequências e outliers/IQR adicionados, usando as funções
  quartis()/iqr() já prontas e testadas no Módulo 1 — faltavam pra
  cobrir o que a sistematização pede pra este módulo (tabela de
  frequências, gráficos, outliers/IQR).
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- Importa o núcleo estatístico próprio (Módulo 1) ---
_PASTA_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_MODULO1 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 1")
if _PASTA_MODULO1 not in sys.path:
    sys.path.insert(0, _PASTA_MODULO1)
from statslocal import quartis, iqr as calcular_iqr, assimetria, media


# Pasta de gráficos da RAIZ do projeto — mesma usada por analise_completa.py,
# não uma pasta nova dentro de "Modulo 2/".
PASTA_GRAFICOS = Path(_PASTA_RAIZ_PROJETO) / "graficos"


def nome_arquivo_seguro(texto: str, max_len: int = 50) -> str:
    """Remove caracteres inválidos para nome de arquivo no Windows."""
    texto = re.sub(r'[\\/*?:"<>|]', '', str(texto))
    return texto.strip()[:max_len] or "sem_nome"


def _selecionar_colunas(df: pd.DataFrame):
    """Deixa o usuário escolher, na tela, quais colunas do dataset usar."""
    st.caption("Escolha quais colunas do dataset representam categoria, subcategoria e valor.")
    colunas = df.columns.tolist()
    colunas_numericas = df.select_dtypes(include="number").columns.tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        coluna_categoria = st.selectbox("Categoria (macro)", colunas, key="m2_categoria")
    with col2:
        coluna_subcategoria = st.selectbox("Subcategoria (micro)", colunas, key="m2_subcategoria")
    with col3:
        opcoes_valor = colunas_numericas or colunas
        coluna_valor = st.selectbox("Valor a somar", opcoes_valor, key="m2_valor")

    return coluna_categoria, coluna_subcategoria, coluna_valor


@st.cache_data(show_spinner=False)
def _resumo_por_categoria(df: pd.DataFrame, coluna_categoria: str, coluna_valor: str) -> pd.Series:
    return df.groupby(coluna_categoria)[coluna_valor].sum().sort_values(ascending=False)


@st.cache_data(show_spinner=False)
def _resumo_subcategoria(
    df: pd.DataFrame,
    categoria,
    coluna_categoria: str,
    coluna_subcategoria: str,
    coluna_valor: str,
) -> Optional[pd.Series]:
    subset = df[df[coluna_categoria] == categoria]
    if subset[coluna_subcategoria].isna().all():
        return None
    return subset.groupby(coluna_subcategoria)[coluna_valor].sum().sort_values(ascending=False)


def grafico_macro_categorias(
    df: pd.DataFrame, coluna_categoria: str, coluna_valor: str, top_n: int = 20
) -> pd.Series:
    """Gráfico 1: visão macro, somando o valor escolhido agrupado pela categoria escolhida."""
    resumo = _resumo_por_categoria(df, coluna_categoria, coluna_valor)

    fig, ax = plt.subplots(figsize=(12, 8))
    try:
        resumo.head(top_n).plot(kind="barh", ax=ax)
        ax.set_title(f"Totais por Categoria (Top {top_n})")
        ax.set_xlabel("Valor total")
        fig.tight_layout()
        st.pyplot(fig)

        PASTA_GRAFICOS.mkdir(exist_ok=True)
        destino = PASTA_GRAFICOS / "grafico1_categorias.png"
        fig.savefig(destino, dpi=150)
        st.caption(f"Gráfico salvo em {destino}")
    finally:
        plt.close(fig)

    return resumo


def _plotar_subcategoria(dados: pd.Series, categoria) -> "plt.Figure":
    fig, ax = plt.subplots(figsize=(10, 6))
    dados.plot(kind="bar", ax=ax)
    ax.set_title(f"Subcategorias: {str(categoria)[:60]}")
    ax.set_ylabel("Valor total")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    return fig


def grafico_subcategoria_interativo(
    df: pd.DataFrame, coluna_categoria: str, coluna_subcategoria: str, coluna_valor: str
) -> None:
    """Mostra o detalhe de UMA categoria por vez, escolhida em um selectbox."""
    categorias = sorted(df[coluna_categoria].dropna().unique(), key=str)
    if not categorias:
        st.info("Não há categorias para detalhar.")
        return

    categoria = st.selectbox("Categoria para detalhar", categorias, key="m2_categoria_detalhe")
    dados = _resumo_subcategoria(df, categoria, coluna_categoria, coluna_subcategoria, coluna_valor)

    if dados is None:
        st.info("Essa categoria não tem subcategorias para detalhar.")
        return

    fig = _plotar_subcategoria(dados, categoria)
    try:
        st.pyplot(fig)
    finally:
        plt.close(fig)


def gerar_todos_os_graficos_subcategoria(
    df: pd.DataFrame, coluna_categoria: str, coluna_subcategoria: str, coluna_valor: str
) -> int:
    """Gera e salva em disco um PNG por categoria (sem exibir todos na tela de uma vez)."""
    PASTA_GRAFICOS.mkdir(exist_ok=True)
    categorias = sorted(df[coluna_categoria].dropna().unique(), key=str)
    if not categorias:
        return 0

    barra = st.progress(0.0)
    gerados = 0

    for i, categoria in enumerate(categorias):
        dados = _resumo_subcategoria(df, categoria, coluna_categoria, coluna_subcategoria, coluna_valor)
        if dados is not None:
            fig = _plotar_subcategoria(dados, categoria)
            try:
                nome = PASTA_GRAFICOS / f"{i:03d}_{nome_arquivo_seguro(str(categoria))}.png"
                fig.savefig(nome, dpi=150)
                gerados += 1
            finally:
                plt.close(fig)
        barra.progress((i + 1) / len(categorias))

    barra.empty()
    return gerados


def tabela_frequencias(df: pd.DataFrame, coluna: str, top_n: int = 15) -> pd.DataFrame:
    """
    Monta a tabela de frequência absoluta e relativa de uma coluna,
    contando as ocorrências manualmente (sem usar um value_counts() pronto).
    """
    contagem = {}
    total = 0
    for valor in df[coluna]:
        if pd.isna(valor):
            continue
        contagem[valor] = contagem.get(valor, 0) + 1
        total += 1

    linhas = [
        {
            "valor": valor,
            "frequencia_absoluta": freq,
            "frequencia_relativa_%": round(100 * freq / total, 2) if total else 0.0,
        }
        for valor, freq in contagem.items()
    ]

    tabela = pd.DataFrame(linhas).sort_values("frequencia_absoluta", ascending=False)
    return tabela.head(top_n).reset_index(drop=True)


def secao_tabela_frequencias(df: pd.DataFrame) -> None:
    st.subheader("2.3 Tabela de frequências")
    colunas_categoricas = df.select_dtypes(exclude="number").columns.tolist()
    if not colunas_categoricas:
        st.info("Não há colunas categóricas no dataset para tabular.")
        return
    coluna = st.selectbox("Coluna para tabela de frequências", colunas_categoricas, key="m2_freq_coluna")
    tabela = tabela_frequencias(df, coluna)
    st.dataframe(tabela, use_container_width=True)


def secao_outliers_iqr(df: pd.DataFrame, coluna_valor: str) -> None:
    """Detecta outliers pela regra do IQR (Q1 - 1.5*IQR / Q3 + 1.5*IQR), usando o Módulo 1."""
    st.subheader("2.4 Outliers (regra do IQR)")
    dados = df[coluna_valor].dropna().tolist()
    if len(dados) < 4:
        st.info("Poucos dados válidos nessa coluna para calcular quartis.")
        return

    q1, q2, q3 = quartis(dados)
    valor_iqr = calcular_iqr(dados)
    limite_inferior = q1 - 1.5 * valor_iqr
    limite_superior = q3 + 1.5 * valor_iqr

    col1, col2, col3 = st.columns(3)
    col1.metric("Q1", f"{q1:.2f}")
    col2.metric("Mediana (Q2)", f"{q2:.2f}")
    col3.metric("Q3", f"{q3:.2f}")
    st.caption(f"IQR = {valor_iqr:.2f} · limites: [{limite_inferior:.2f}, {limite_superior:.2f}]")

    outliers = df[(df[coluna_valor] < limite_inferior) | (df[coluna_valor] > limite_superior)]
    st.write(f"**{len(outliers)}** valores fora do intervalo (de {len(dados)} linhas com dado válido).")
    if not outliers.empty:
        st.dataframe(outliers[[coluna_valor]].sort_values(coluna_valor), use_container_width=True)

def grafico_boxplot(df: pd.DataFrame, coluna_valor: str) -> None:
    """Gráfico 2.5: boxplot da coluna numérica escolhida."""
    dados = df[coluna_valor].dropna()
    if dados.empty:
        st.info("Não há dados válidos para montar o boxplot.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    try:
        ax.boxplot(dados, vert=False, patch_artist=True,
                   boxprops=dict(facecolor="#4C72B0", alpha=0.6))
        ax.set_title(f"Boxplot — {coluna_valor}")
        ax.set_xlabel(coluna_valor)
        fig.tight_layout()
        st.pyplot(fig)

        PASTA_GRAFICOS.mkdir(exist_ok=True)
        destino = PASTA_GRAFICOS / f"boxplot_{nome_arquivo_seguro(coluna_valor)}.png"
        fig.savefig(destino, dpi=150)
        st.caption(f"Gráfico salvo em {destino}")
    finally:
        plt.close(fig)


def secao_boxplot(df: pd.DataFrame, coluna_valor: str) -> None:
    st.subheader("2.5 Boxplot")
    grafico_boxplot(df, coluna_valor)


def grafico_pizza_categorias(
    df: pd.DataFrame, coluna_categoria: str, coluna_valor: str, top_n: int = 6
) -> None:
    """Gráfico 2.6: pizza com as top_n categorias e o restante agrupado em 'Outros'."""
    resumo = _resumo_por_categoria(df, coluna_categoria, coluna_valor)
    if resumo.empty:
        st.info("Não há dados suficientes para montar o gráfico de pizza.")
        return

    principais = resumo.head(top_n)
    restante = resumo.iloc[top_n:].sum()
    if restante > 0:
        principais = pd.concat([principais, pd.Series({"Outros": restante})])

    fig, ax = plt.subplots(figsize=(8, 8))
    try:
        ax.pie(
            principais.values,
            labels=principais.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.set_title(f"Distribuição por {coluna_categoria} (Top {top_n} + Outros)")
        ax.axis("equal")
        fig.tight_layout()
        st.pyplot(fig)

        PASTA_GRAFICOS.mkdir(exist_ok=True)
        destino = PASTA_GRAFICOS / f"pizza_{nome_arquivo_seguro(coluna_categoria)}.png"
        fig.savefig(destino, dpi=150)
        st.caption(f"Gráfico salvo em {destino}")
    finally:
        plt.close(fig)


def secao_grafico_pizza(df: pd.DataFrame, coluna_categoria: str, coluna_valor: str) -> None:
    st.subheader("2.6 Gráfico de pizza")
    grafico_pizza_categorias(df, coluna_categoria, coluna_valor)


def secao_interpretacao_automatica(df: pd.DataFrame, coluna_valor: str) -> None:
    """Gera um texto automático interpretando a forma da distribuição (assimetria)."""
    st.subheader("2.7 Interpretação automática")
    dados = df[coluna_valor].dropna().tolist()
    if len(dados) < 3:
        st.info("Poucos dados válidos para interpretar a distribuição.")
        return

    media_dados = media(dados)
    _, mediana_dados, _ = quartis(dados)
    coef_assimetria = assimetria(dados)

    col1, col2 = st.columns(2)
    col1.metric("Média", f"{media_dados:.2f}")
    col2.metric("Mediana", f"{mediana_dados:.2f}")
    st.metric("Coeficiente de assimetria", f"{coef_assimetria:.3f}")

    if abs(coef_assimetria) < 0.5:
        texto = "A distribuição é aproximadamente **simétrica** (assimetria próxima de zero)."
    elif coef_assimetria >= 0.5:
        texto = (
            "A distribuição apresenta **assimetria positiva (à direita)**: a cauda direita é "
            "mais longa e a média tende a ficar acima da mediana, geralmente puxada por "
            "valores extremos altos."
        )
    else:
        texto = (
            "A distribuição apresenta **assimetria negativa (à esquerda)**: a cauda esquerda é "
            "mais longa e a média tende a ficar abaixo da mediana."
        )

    st.write(texto)

def modulo2_estatistica_interativa(df: pd.DataFrame) -> None:
    """Ponto de entrada do Módulo 2 -- chamado a partir do app.py (Módulo 0)."""
    st.header("Módulo 2 — Estatística Descritiva Interativa")

    coluna_categoria, coluna_subcategoria, coluna_valor = _selecionar_colunas(df)

    st.subheader("2.1 Visão macro por categoria")
    grafico_macro_categorias(df, coluna_categoria, coluna_valor)

    st.divider()

    st.subheader("2.2 Detalhe por subcategoria")
    grafico_subcategoria_interativo(df, coluna_categoria, coluna_subcategoria, coluna_valor)

    if st.button("Gerar e salvar gráficos de TODAS as categorias em disco"):
        with st.spinner("Gerando gráficos..."):
            total = gerar_todos_os_graficos_subcategoria(
                df, coluna_categoria, coluna_subcategoria, coluna_valor
            )
        st.success(f"{total} gráficos de subcategoria salvos em '{PASTA_GRAFICOS}/'.")

    st.divider()
    secao_tabela_frequencias(df)

    st.divider()
    secao_outliers_iqr(df, coluna_valor)

    st.divider()
    secao_boxplot(df, coluna_valor)

    st.divider()
    secao_grafico_pizza(df, coluna_categoria, coluna_valor)

    st.divider()
    secao_interpretacao_automatica(df, coluna_valor)