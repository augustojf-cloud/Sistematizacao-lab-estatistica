import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import statslocal as ms


def render_modulo5(df: pd.DataFrame):
    st.header("Módulo 5 - Correlação e Regressão Linear")

    colunas_numericas = df.select_dtypes(include=np.number).columns.tolist()

    # remove colunas "constantes" (mesmo valor em todas as linhas, ex.: ano do
    # ciclo do dataset) -- sem variação, não dá pra calcular correlação/regressão
    colunas_numericas = [c for c in colunas_numericas if df[c].nunique(dropna=True) > 1]

    if len(colunas_numericas) < 2:
        st.warning("O dataset precisa de pelo menos 2 variáveis numéricas com variação para essa análise.")
        return

    col1, col2 = st.columns(2)
    with col1:
        var_x = st.selectbox("Variável X (independente)", colunas_numericas, index=0)
    with col2:
        opcoes_y = [c for c in colunas_numericas if c != var_x]
        var_y = st.selectbox("Variável Y (dependente)", opcoes_y, index=0)

    dados_x = df[var_x].dropna()
    dados_y = df[var_y].dropna()

    # garante que as duas séries fiquem alinhadas (mesmos índices, sem NaN em nenhuma das duas)
    dados_validos = df[[var_x, var_y]].dropna()
    x = dados_validos[var_x].tolist()
    y = dados_validos[var_y].tolist()

    if len(x) < 2:
        st.warning("Não há pares de dados suficientes (sem valores ausentes) para essas duas variáveis.")
        return

    try:
        r = ms.correlacao_pearson(x, y)
        a, b = ms.regressao_linear_simples(x, y)
        r2 = ms.r_quadrado(x, y)
    except ValueError as erro:
        st.warning(f"Não foi possível calcular a correlação/regressão para essas variáveis: {erro}")
        return

    st.subheader("Diagrama de Dispersão")
    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.6, edgecolor="black")

    x_min, x_max = min(x), max(x)
    x_reta = [x_min, x_max]
    y_reta = [a + b * xi for xi in x_reta]
    ax.plot(x_reta, y_reta, color="red", linewidth=2, label="Reta de regressão")

    ax.set_xlabel(var_x)
    ax.set_ylabel(var_y)
    ax.legend()
    st.pyplot(fig)

    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Correlação (r)", f"{r:.4f}")
    col2.metric("R²", f"{r2:.4f}")
    col3.metric("Coeficiente angular (b)", f"{b:.4f}")

    sinal = "+" if a >= 0 else "-"
    st.write(f"**Equação da reta:** {var_y} = {b:.4f} · {var_x} {sinal} {abs(a):.4f}")

    if abs(r) >= 0.7:
        forca = "forte"
    elif abs(r) >= 0.3:
        forca = "moderada"
    else:
        forca = "fraca"
    direcao = "positiva" if r > 0 else "negativa" if r < 0 else "nula"

    st.write(
        f"A correlação entre **{var_x}** e **{var_y}** é **{forca}** e **{direcao}** "
        f"(r = {r:.4f}). O modelo explica aproximadamente **{r2*100:.1f}%** "
        f"da variação de {var_y} (R²)."
    )

    st.info(
        "⚠️ Correlação não implica causalidade. Um valor alto de r indica que as "
        "duas variáveis se movem juntas, mas não prova que uma seja a causa da outra."
    )

    st.subheader("Predição interativa")
    valor_x = st.number_input(f"Digite um valor de {var_x} para prever {var_y}", value=float(x_min))
    valor_previsto = a + b * valor_x
    st.success(f"Predição: {var_y} ≈ {valor_previsto:.4f}")