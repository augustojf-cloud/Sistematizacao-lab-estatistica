# 1. CRIA AS CATEGORIAS DO GRÁFICO QUE SERÁ ALIMENTADO PELO DATASET, TENDO CATEGORIAS MACRO E SUBCATEGORIAS MICRO

import matplotlib
matplotlib.use('Agg')  # gera os gráficos direto em arquivo, sem abrir janela — mais rápido para gerar muitos de uma vez
import matplotlib.pyplot as plt
import os
import re

PASTA_GRAFICOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'graficos')

def nome_arquivo_seguro(texto, max_len=50):
    """Remove caracteres inválidos para nome de arquivo no Windows."""
    texto = re.sub(r'[\\/*?:"<>|]', '', str(texto))
    return texto.strip()[:max_len]


def grafico_macro_categorias(df_colunas, top_n=20):
    """Gráfico 1: visão macro, somando todas as subcategorias dentro de cada categoria."""
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    resumo = df_colunas.groupby('categoria')['valor_total'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 8))
    resumo.head(top_n).plot(kind='barh')
    plt.title(f'Totais por Categoria (Top {top_n})')
    plt.xlabel('Valor total')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}/grafico1_categorias.png', dpi=150)
    plt.close()
    print(f"Gráfico 1 salvo em {PASTA_GRAFICOS}/grafico1_categorias.png")
    return resumo


def graficos_subcategorias(df_colunas):
    """Gráfico 2: um gráfico por categoria, detalhando suas subcategorias."""
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    categorias = df_colunas['categoria'].unique()
    gerados = 0

    for i, categoria in enumerate(categorias):
        subset = df_colunas[df_colunas['categoria'] == categoria]
        if subset['subcategoria'].isna().all():
            continue  # categoria sem subdivisão, não precisa de gráfico de detalhe

        dados = subset.groupby('subcategoria')['valor_total'].sum().sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        dados.plot(kind='bar')
        plt.title(f'Subcategorias: {categoria[:60]}')
        plt.ylabel('Valor total')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        nome = f"{PASTA_GRAFICOS}/{i:03d}_{nome_arquivo_seguro(categoria)}.png"
        plt.savefig(nome, dpi=150)
        plt.close()
        gerados += 1

    print(f"{gerados} gráficos de subcategoria salvos na pasta '{PASTA_GRAFICOS}/'.")

    