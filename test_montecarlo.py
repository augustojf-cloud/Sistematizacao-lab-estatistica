"""
Testes automatizados do Módulo 2 (simulação de Monte Carlo).

Como envolve sorteios aleatórios, usamos uma "semente" (seed) fixa em
todo teste — isso faz com que os "sorteios aleatórios" sejam sempre os
mesmos toda vez que o teste rodar, tornando o resultado reproduzível
(sem isso, o teste passaria ou falharia de forma diferente a cada
execução, o que não serve para validação automatizada).

As comparações aqui usam tolerâncias maiores que as do Módulo 1,
porque este é um resultado ESTATÍSTICO/probabilístico (converge para
o valor esperado conforme n cresce), e não um cálculo matemático
exato como média ou variância.

Rodar com:
    pytest test_montecarlo.py -v
"""

import pytest

import montecarlo as mc
from statslocal import media, variancia, desvio_padrao

# População sintética conhecida: números de 1 a 100.
# Média teórica: (1 + 100) / 2 = 50.5
POPULACAO = list(range(1, 101))
MEDIA_REAL = media(POPULACAO)


def test_lei_dos_grandes_numeros_converge_para_media_real():
    medias_acumuladas = mc.lei_dos_grandes_numeros(POPULACAO, n_sorteios=3000, semente=42)

    # Tem que ter uma média acumulada para cada sorteio
    assert len(medias_acumuladas) == 3000

    # A média acumulada DEPOIS DE POUCOS sorteios costuma estar mais
    # longe da média real do que a média DEPOIS DE MUITOS sorteios.
    # Comparamos o "erro" (distância até a média real) logo no início
    # com o erro no final: o final deve estar bem mais perto.
    erro_inicial = abs(medias_acumuladas[9] - MEDIA_REAL)      # após 10 sorteios
    erro_final = abs(medias_acumuladas[-1] - MEDIA_REAL)        # após 3000 sorteios
    assert erro_final < erro_inicial

    # Com 3000 sorteios (com reposição) de uma população de média
    # 50.5, a média acumulada final deve estar bem próxima da real.
    assert medias_acumuladas[-1] == pytest.approx(MEDIA_REAL, abs=1.5)


def test_lei_dos_grandes_numeros_primeiro_valor_e_o_primeiro_sorteio():
    # Depois de UM único sorteio, a "média acumulada" é o próprio
    # valor sorteado (não há o que fazer média ainda).
    medias_acumuladas = mc.lei_dos_grandes_numeros(POPULACAO, n_sorteios=1, semente=7)
    assert medias_acumuladas[0] in POPULACAO


def test_teorema_central_limite_media_das_medias_proxima_da_media_real():
    medias_das_amostras = mc.teorema_central_limite(
        POPULACAO, tamanho_amostra=30, n_simulacoes=2000, semente=123
    )

    assert len(medias_das_amostras) == 2000

    # A média de todas as médias amostrais deve ficar bem próxima da
    # média real da população (propriedade de "estimador não-viesado").
    media_das_medias = media(medias_das_amostras)
    assert media_das_medias == pytest.approx(MEDIA_REAL, abs=0.5)


def test_teorema_central_limite_desvio_padrao_das_medias_segue_erro_padrao():
    tamanho_amostra = 30
    medias_das_amostras = mc.teorema_central_limite(
        POPULACAO, tamanho_amostra=tamanho_amostra, n_simulacoes=2000, semente=123
    )

    # Erro padrão teórico: desvio padrão da população / raiz(tamanho da amostra).
    desvio_populacao = desvio_padrao(POPULACAO, amostral=False)
    erro_padrao_teorico = desvio_populacao / (tamanho_amostra ** 0.5)

    desvio_observado = desvio_padrao(medias_das_amostras, amostral=True)

    # Tolerância generosa (20%) porque é uma estimativa baseada em
    # sorteio aleatório, não um cálculo exato.
    assert desvio_observado == pytest.approx(erro_padrao_teorico, rel=0.2)
