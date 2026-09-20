
import numpy as np
from scipy import stats as sp_stats
import pytest

import statslocal as ms

# Tolerância numérica usada em todas as comparações (documentada aqui,
# conforme exigido pelo enunciado).
TOL = 1e-9

DADOS = [4, 8, 15, 16, 23, 42, 8, 4, 16, 10]
DADOS_X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DADOS_Y = [2.1, 3.9, 6.2, 7.8, 10.1, 12.3, 13.9, 16.2, 18.0, 19.8]


def test_media():
    assert ms.media(DADOS) == pytest.approx(np.mean(DADOS), abs=TOL)


def test_mediana():
    assert ms.mediana(DADOS) == pytest.approx(np.median(DADOS), abs=TOL)


def test_moda():
    # scipy.stats.mode retorna a menor moda em caso de empate
    resultado_scipy = sp_stats.mode(DADOS, keepdims=False)
    minha_moda = ms.moda(DADOS)
    assert resultado_scipy.mode in minha_moda


def test_amplitude():
    esperado = max(DADOS) - min(DADOS)
    assert ms.amplitude(DADOS) == pytest.approx(esperado, abs=TOL)


def test_variancia_amostral():
    assert ms.variancia(DADOS, amostral=True) == pytest.approx(
        np.var(DADOS, ddof=1), abs=TOL
    )


def test_variancia_populacional():
    assert ms.variancia(DADOS, amostral=False) == pytest.approx(
        np.var(DADOS, ddof=0), abs=TOL
    )


def test_desvio_padrao_amostral():
    assert ms.desvio_padrao(DADOS, amostral=True) == pytest.approx(
        np.std(DADOS, ddof=1), abs=TOL
    )


def test_desvio_padrao_populacional():
    assert ms.desvio_padrao(DADOS, amostral=False) == pytest.approx(
        np.std(DADOS, ddof=0), abs=TOL
    )


def test_coef_variacao():
    esperado = np.std(DADOS, ddof=1) / np.mean(DADOS)
    assert ms.coef_variacao(DADOS, amostral=True) == pytest.approx(esperado, abs=TOL)


def test_percentil():
    for p in [10, 25, 50, 75, 90]:
        assert ms.percentil(DADOS, p) == pytest.approx(
            np.percentile(DADOS, p), abs=TOL
        )


def test_quartis():
    q1, q2, q3 = ms.quartis(DADOS)
    assert q1 == pytest.approx(np.percentile(DADOS, 25), abs=TOL)
    assert q2 == pytest.approx(np.percentile(DADOS, 50), abs=TOL)
    assert q3 == pytest.approx(np.percentile(DADOS, 75), abs=TOL)


def test_iqr():
    esperado = np.percentile(DADOS, 75) - np.percentile(DADOS, 25)
    assert ms.iqr(DADOS) == pytest.approx(esperado, abs=TOL)


def test_covariancia():
    esperado = np.cov(DADOS_X, DADOS_Y, ddof=1)[0][1]
    assert ms.covariancia(DADOS_X, DADOS_Y, amostral=True) == pytest.approx(
        esperado, abs=1e-6
    )


def test_correlacao_pearson():
    esperado, _ = sp_stats.pearsonr(DADOS_X, DADOS_Y)
    assert ms.correlacao_pearson(DADOS_X, DADOS_Y) == pytest.approx(esperado, abs=1e-6)


def test_regressao_linear_simples():
    resultado_scipy = sp_stats.linregress(DADOS_X, DADOS_Y)
    a, b = ms.regressao_linear_simples(DADOS_X, DADOS_Y)
    assert b == pytest.approx(resultado_scipy.slope, abs=1e-6)
    assert a == pytest.approx(resultado_scipy.intercept, abs=1e-6)


def test_r_quadrado():
    resultado_scipy = sp_stats.linregress(DADOS_X, DADOS_Y)
    r2_esperado = resultado_scipy.rvalue ** 2
    assert ms.r_quadrado(DADOS_X, DADOS_Y) == pytest.approx(r2_esperado, abs=1e-6)


def test_lista_vazia_levanta_erro():
    with pytest.raises(ValueError):
        ms.media([])


def test_densidade_normal():
    m = ms.media(DADOS)
    dp = ms.desvio_padrao(DADOS, amostral=True)
    for x in [0, 5, 10, 15, 20]:
        esperado = sp_stats.norm.pdf(x, loc=m, scale=dp)
        assert ms.densidade_normal(x, m, dp) == pytest.approx(esperado, abs=TOL)


def test_densidade_uniforme():
    minimo, maximo = min(DADOS), max(DADOS)
    for x in [minimo - 1, minimo, (minimo + maximo) / 2, maximo, maximo + 1]:
        esperado = sp_stats.uniform.pdf(x, loc=minimo, scale=maximo - minimo)
        assert ms.densidade_uniforme(x, minimo, maximo) == pytest.approx(esperado, abs=TOL)


def test_densidade_exponencial():
    taxa = 1 / ms.media(DADOS)
    for x in [-1, 0, 5, 10, 20]:
        esperado = sp_stats.expon.pdf(x, scale=1 / taxa)
        assert ms.densidade_exponencial(x, taxa) == pytest.approx(esperado, abs=TOL)


def test_assimetria():
    esperado = sp_stats.skew(DADOS, bias=True)
    assert ms.assimetria(DADOS) == pytest.approx(esperado, abs=TOL)


def test_assimetria_poucos_dados_levanta_erro():
    with pytest.raises(ValueError):
        ms.assimetria([1, 2])
