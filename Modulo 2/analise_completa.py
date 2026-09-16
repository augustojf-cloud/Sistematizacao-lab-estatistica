# SERÁ REALIZADO O RAIO-X DO DATASET, COM UMA ANÁLISE GRÁFICAE E ESTATÍSTICA LEVANDO EM CONTA O MÓDULO0 E MÓDULO1.
# OS CÓDIGOS SERÃO ORGANIZADOS EM FUNÇÕES, PARA QUE POSSAM SER REUTILIZADOS EM OUTROS MÓDULOS.
# A BRANCH GRÁFICOS É RESPONSÁVEL PELA ANÁLISE GRÁFICA, ENQUANTO A BRANCH ESTATÍSTICA É RESPONSÁVEL PELA ANÁLISE ESTATÍSTICA, PORÉM A BRANCH GRÁFICOS LEVA EM CONTA TODOS OS DADOS ESTATÍSTICOS DA BRANCH ANTERIOR.

'''python'''
import matplotlib
import  matplotlib.pyplot as plt
import os
import sys
_PASTA_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_MODULO0 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 0")
_PASTA_MODULO1 = os.path.join(_PASTA_RAIZ_PROJETO, "Modulo 1")
for _pasta in (_PASTA_RAIZ_PROJETO, _PASTA_MODULO0, _PASTA_MODULO1):
    if _pasta not in sys.path:
        sys.path.insert(0, _pasta)
import statslocal as ms
from modulo0_dataset import carregar_dataset, CAMINHO_ARQUIVO
from Modulo2_graficos import grafico_macro_categorias, graficos_subcategorias # Chama os módulos de gráficos para gerar os gráficos de análise


df = carregar_dataset(CAMINHO_ARQUIVO)

# 1. Carregar o dataset já usado 

import pandas as pd

# 2. Exporta a lista completa de colunas para um arquivo (mais fácil de consultar)
_CAMINHO_COLUNAS_DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colunas_dataset.txt')
with open(_CAMINHO_COLUNAS_DATASET, 'w', encoding='utf-8') as f:
    for i, coluna in enumerate(df.columns):
        f.write(f"{i}: {coluna}\n")

print(f"{len(df.columns)} colunas salvas em colunas_dataset.txt")

# 3. Separa cada nome de coluna em categoria principal e subcategoria (quando existir o "|")
estrutura = []
for i, coluna in enumerate(df.columns):
    partes = [p.strip() for p in str(coluna).split('|')]
    estrutura.append({
        'indice': i,
        'categoria': partes[0],
        'subcategoria': partes[1] if len(partes) > 1 else None,
        'nome_completo': coluna
    })

df_colunas = pd.DataFrame(estrutura)
_CAMINHO_MAPA_COLUNAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapa_colunas.xlsx')
df_colunas.to_excel(_CAMINHO_MAPA_COLUNAS, index=False)
print("Mapa de colunas salvo em mapa_colunas.xlsx — abra no Excel para filtrar por categoria.")

def procurar_coluna(palavra_chave):
    encontradas = [(i, c) for i, c in enumerate(df.columns) if palavra_chave.lower() in str(c).lower()]
    for i, c in encontradas:
        print(f"{i}: {c}")
    return encontradas

procurar_coluna("visita")

# 4. Organiza o dataset para análise, nomeando as colunas e definindo as linhas compativeis com cada coluna real do dataset.





# 5. Calcula o valor total de cada coluna e junta ao mapa de categorias
valores_numericos = df.apply(pd.to_numeric, errors='coerce')
totais_por_coluna = valores_numericos.sum()

df_colunas['valor_total'] = df_colunas['nome_completo'].map(totais_por_coluna)

# Remove colunas identificadoras (não são quantidades, e distorcem o gráfico macro)
CATEGORIAS_IDENTIFICADORAS = ['CEP', 'Código IBGE', 'Ano']  # ajuste se notar outras assim
df_colunas_grafico = df_colunas[~df_colunas['categoria'].isin(CATEGORIAS_IDENTIFICADORAS)]

# 6. Gera os gráficos (macro por categoria e detalhamento por subcategoria)

resumo_categorias = grafico_macro_categorias(df_colunas_grafico)
graficos_subcategorias(df_colunas)  
