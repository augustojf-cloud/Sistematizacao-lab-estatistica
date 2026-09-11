"""
========================================================================
 SISTEMATIZAÇÃO - Laboratório de Estatística em Python
 Módulo 3: Probabilidade e Simulação (Monte Carlo)
========================================================================

Este módulo demonstra, na prática, dois resultados fundamentais da
estatística usando simulação (sorteios aleatórios repetidos):

1. LEI DOS GRANDES NÚMEROS (LGN)
   Quanto mais valores você sorteia de uma população, mais a média
   desses sorteios se aproxima da média real da população inteira.

2. TEOREMA CENTRAL DO LIMITE (TCL)
   Se você sorteia várias amostras (todas do mesmo tamanho) e calcula
   a média de cada uma, a distribuição dessas médias tende a um
   formato de sino (distribuição normal) — não importa qual seja o
   formato da distribuição original dos dados.

Assim como no Módulo 1, os cálculos de média usados aqui vêm do nosso
próprio código (statslocal.py), não de bibliotecas prontas. O único
uso de biblioteca externa aqui é o módulo "random" do Python, que é
necessário para GERAR os sorteios aleatórios (isso não é uma função
estatística pronta, é geração de números aleatórios, que é a base de
qualquer simulação de Monte Carlo).
"""

import random

import os
import sys
_PASTA_MODULO1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Modulo 1")
if _PASTA_MODULO1 not in sys.path:
    sys.path.insert(0, _PASTA_MODULO1)
from statslocal import media


def amostra_aleatoria(dados, tamanho, com_reposicao=True, semente=None):
    """
    Sorteia 'tamanho' valores da lista 'dados'.

    com_reposicao=True  -> um mesmo valor pode ser sorteado mais de uma
                            vez (é o que a simulação de Monte Carlo usa
                            normalmente, pois trata 'dados' como uma
                            representação da população).
    com_reposicao=False -> cada valor só pode ser sorteado uma vez
                            (equivalente a tirar uma amostra sem
                            devolver o item sorteado).
    """
    if semente is not None:
        random.seed(semente)
    if com_reposicao:
        return [random.choice(dados) for _ in range(tamanho)]
    return random.sample(dados, tamanho)


def lei_dos_grandes_numeros(dados, n_sorteios, semente=None):
    """
    Simula a Lei dos Grandes Números.

    Sorteia, um de cada vez (com reposição), 'n_sorteios' valores da
    lista 'dados'. A cada novo sorteio, recalcula a média de tudo que
    já foi sorteado até agora.

    Retorna a lista dessas médias acumuladas (uma para cada sorteio).
    O gráfico dessa lista deve mostrar uma linha que "treme" bastante
    no início e vai se estabilizando conforme o eixo x cresce.

    Observação de implementação: em vez de recalcular a média do zero
    a cada passo (o que seria O(n) por passo, O(n²) no total), usamos
    a fórmula de atualização incremental da média:

        média_nova = média_antiga + (novo_valor - média_antiga) / n

    Essa fórmula é equivalente a somar tudo e dividir por n, só que
    calculada de forma progressiva — o resultado matemático é
    idêntico, mas o cálculo fica muito mais rápido para n grande.
    """
    if semente is not None:
        random.seed(semente)

    medias_acumuladas = []
    media_atual = 0.0
    for n in range(1, n_sorteios + 1):
        novo_valor = random.choice(dados)
        media_atual = media_atual + (novo_valor - media_atual) / n
        medias_acumuladas.append(media_atual)

    return medias_acumuladas


def teorema_central_limite(dados, tamanho_amostra, n_simulacoes, semente=None):
    """
    Simula o Teorema Central do Limite.

    Sorteia 'n_simulacoes' amostras independentes (cada uma com
    reposição, de tamanho 'tamanho_amostra'), calcula a média de cada
    amostra usando a nossa própria função media() (statslocal.py), e
    devolve a lista com todas essas médias.

    Ao plotar um histograma dessa lista, o formato deve se aproximar
    de um sino (distribuição normal), independente do formato da
    distribuição de 'dados' originalmente.
    """
    if semente is not None:
        random.seed(semente)

    medias_das_amostras = []
    for _ in range(n_simulacoes):
        amostra = [random.choice(dados) for _ in range(tamanho_amostra)]
        medias_das_amostras.append(media(amostra))

    return medias_das_amostras
