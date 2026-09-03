"""
========================================================================
 SISTEMATIZAÇÃO - Laboratório de Estatística em Python
 Módulo 0: Carregamento e Inspeção do Dataset Real
 Disciplina: Lógica / Lógica Matemática (ADS - UniCEUB)

 Dataset escolhido: SISDEPEN - Levantamento Nacional de Informações
 Penitenciárias, dados de 2025 (Departamento Penitenciário Nacional/MJ)
========================================================================

O que este módulo faz:
1. Carrega o arquivo CSV do SISDEPEN para dentro do Python (em uma
   estrutura chamada "DataFrame", que é como uma planilha do Excel
   dentro do código).
2. Faz uma primeira inspeção dos dados: quantas linhas e colunas
   existem, quais são os nomes das colunas, quais tipos de dado cada
   coluna tem (texto, número, etc.), se há valores ausentes (células
   vazias) e se há linhas duplicadas.

Este é o ponto de partida de todos os módulos seguintes (estatística
descritiva, Monte Carlo, distribuições, correlação/regressão): eles
vão reutilizar o DataFrame que este módulo carrega e valida aqui.
"""

# ------------------------------------------------------------------
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ------------------------------------------------------------------
# "pandas" é a biblioteca padrão do Python para trabalhar com dados
# em formato de tabela (linhas e colunas). Chamamos ela de "pd" só
# para não precisar digitar "pandas" toda vez.
import pandas as pd


# ------------------------------------------------------------------
# 2. CONFIGURAÇÃO
# ------------------------------------------------------------------
# Coloque aqui o nome (ou caminho completo) do arquivo baixado do
# SISDEPEN. Ele precisa estar na mesma pasta deste script, ou você
# deve indicar o caminho completo
# (ex: "C:/Users/SeuNome/Downloads/sisdepen_2025.xlsx")
CAMINHO_ARQUIVO = r"D:\Augusto\Documentos pessoais\Faculdade\Análise e desenvolvimento de sistemas - ADS\Modulo 0 - dataset\SISDEPEN.xlsx"

NOME_ABA = "Sheet1"  # Nome da aba do Excel que contém os dados

SEPARADOR = ";"
CODIFICACAO = "latin1"


# ------------------------------------------------------------------
# 3. FUNÇÃO: CARREGAR O DATASET
# ------------------------------------------------------------------
# Uma "função" é um bloco de código reutilizável. Aqui, criamos uma
# função chamada carregar_dataset que recebe o caminho do arquivo e
# devolve o DataFrame (a tabela) já carregado.
#
# Esta versão detecta sozinha se o arquivo é Excel (.xlsx/.xls) ou
# CSV (texto), olhando para a extensão do nome do arquivo, e usa a
# função certa do pandas em cada caso: pd.read_excel() ou pd.read_csv().
def carregar_dataset(caminho, separador=SEPARADOR, codificacao=CODIFICACAO, aba=NOME_ABA):
    # .lower() deixa tudo minúsculo, para não depender de o arquivo
    # estar salvo como ".XLSX" ou ".xlsx", por exemplo.
    extensao = caminho.lower().split(".")[-1]

    # "try/except" é uma estrutura de tratamento de erro: o Python
    # tenta executar o que está dentro do "try"; se der erro, ele
    # não trava o programa, e sim executa o que está no "except"
    # correspondente, mostrando uma mensagem clara do problema.
    try:
        if extensao in ("xlsx", "xls"):
            # Arquivo Excel: não tem separador nem codificação, mas
            # pode ter várias abas — por isso o parâmetro sheet_name.
            df = pd.read_excel(caminho, sheet_name=aba)
        elif extensao == "csv":
            df = pd.read_csv(caminho, sep=separador, encoding=codificacao)
        else:
            print(f"ERRO: extensão '.{extensao}' não reconhecida. Use um arquivo .csv, .xlsx ou .xls.")
            return None

        print(f"Dataset carregado com sucesso: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        return df

    except FileNotFoundError:
        print(f"ERRO: arquivo '{caminho}' não foi encontrado. Verifique o nome/caminho.")
        return None
    except UnicodeDecodeError:
        print("ERRO: problema de codificação de caracteres. Tente trocar CODIFICACAO para 'utf-8' ou 'cp1252'.")
        return None
    except ImportError:
        print("ERRO: falta instalar a biblioteca 'openpyxl' para ler arquivos Excel.")
        print("No terminal, rode: pip install openpyxl")
        return None
    except Exception as erro:
        print(f"ERRO inesperado ao carregar o dataset: {erro}")
        return None


# ------------------------------------------------------------------
# 4. FUNÇÃO: INSPECIONAR O DATASET
# ------------------------------------------------------------------
# Esta função recebe o DataFrame já carregado e imprime um raio-x
# inicial dos dados. Cada bloco abaixo responde a uma pergunta básica
# que todo trabalho de estatística precisa responder antes de
# analisar qualquer coisa.
def inspecionar_dataset(df):

    print("\n=== 4.1 Primeiras linhas do dataset ===")
    # .head() mostra, por padrão, as 5 primeiras linhas — serve para
    # "dar uma olhada" rápida no formato dos dados.
    print(df.head())

    print("\n=== 4.2 Dimensão do dataset ===")
    # .shape devolve uma dupla (quantidade de linhas, quantidade de colunas)
    print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")

    print("\n=== 4.3 Nome de todas as colunas ===")
    print(df.columns.tolist())

    print("\n=== 4.4 Tipos de dado de cada coluna ===")
    # .info() mostra, para cada coluna, se ela é número inteiro (int),
    # número decimal (float) ou texto (object), além de quantos
    # valores não-vazios existem em cada uma.
    print(df.info())

    print("\n=== 4.5 Estatísticas descritivas das colunas numéricas ===")
    # .describe() calcula automaticamente média, desvio-padrão,
    # mínimo, máximo e os quartis de cada coluna numérica. Isso é
    # a base do módulo de "estatística descritiva" que vem a seguir.
    print(df.describe())

    print("\n=== 4.6 Valores ausentes (células vazias) por coluna ===")
    # .isnull() marca True/False para cada célula (vazia ou não);
    # .sum() soma quantos "True" (vazios) existem em cada coluna.
    print(df.isnull().sum())

    print("\n=== 4.7 Linhas duplicadas ===")
    # .duplicated() marca True para linhas repetidas; .sum() conta quantas são.
    print(f"Total de linhas duplicadas: {df.duplicated().sum()}")


# ------------------------------------------------------------------
# 5. EXECUÇÃO PRINCIPAL
# ------------------------------------------------------------------
# Este bloco só roda quando o arquivo é executado diretamente
# (e não quando é apenas importado por outro módulo, como o
# Módulo 1 de estatística descritiva que você vai construir depois).
if __name__ == "__main__":
    df = carregar_dataset(CAMINHO_ARQUIVO)

    if df is not None:
        inspecionar_dataset(df)
    else:
        print("\nNão foi possível prosseguir: corrija o carregamento do arquivo antes de continuar.")
