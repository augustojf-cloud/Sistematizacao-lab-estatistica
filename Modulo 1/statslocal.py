"""
Biblioteca estatística  (Módulo 1)
"""

import math
from typing import List, Sequence, Tuple


# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------

def _validar_nao_vazio(dados: Sequence[float]) -> None:
    if dados is None or len(dados) == 0:
        raise ValueError("A lista de dados não pode estar vazia.")


def _ordenar(dados: Sequence[float]) -> List[float]:
    return sorted(dados)


# ---------------------------------------------------------------------------
# Medidas de tendência central
# ---------------------------------------------------------------------------

def media(dados: Sequence[float]) -> float:
    """Média aritmética: soma dos valores dividida pela quantidade."""
    _validar_nao_vazio(dados)
    soma = 0.0
    for x in dados:
        soma += x
    return soma / len(dados)


def mediana(dados: Sequence[float]) -> float:
    """Valor central da lista ordenada (ou média dos dois centrais, se par)."""
    _validar_nao_vazio(dados)
    ordenados = _ordenar(dados)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 1:
        return float(ordenados[meio])
    else:
        return (ordenados[meio - 1] + ordenados[meio]) / 2.0


def moda(dados: Sequence[float]) -> List[float]:
    """
    Valor(es) mais frequente(s). Retorna uma lista porque pode haver
    mais de uma moda (distribuição multimodal).
    """
    _validar_nao_vazio(dados)
    contagem = {}
    for x in dados:
        contagem[x] = contagem.get(x, 0) + 1

    freq_max = max(contagem.values())
    modas = [valor for valor, freq in contagem.items() if freq == freq_max]

    # Se todos os valores aparecem com a mesma frequência, não há moda "real"
    if freq_max == 1:
        return []
    return sorted(modas)


# ---------------------------------------------------------------------------
# Medidas de dispersão
# ---------------------------------------------------------------------------

def amplitude(dados: Sequence[float]) -> float:
    """Diferença entre o maior e o menor valor."""
    _validar_nao_vazio(dados)
    return max(dados) - min(dados)


def variancia(dados: Sequence[float], amostral: bool = True) -> float:
    """
    Variância. Por padrão, amostral (divide por n-1).
    Use amostral=False para variância populacional (divide por n).
    """
    _validar_nao_vazio(dados)
    n = len(dados)
    if amostral and n < 2:
        raise ValueError("Variância amostral requer ao menos 2 valores.")

    m = media(dados)
    soma_quadrados = 0.0
    for x in dados:
        soma_quadrados += (x - m) ** 2

    denominador = (n - 1) if amostral else n
    return soma_quadrados / denominador


def desvio_padrao(dados: Sequence[float], amostral: bool = True) -> float:
    """Raiz quadrada da variância (amostral ou populacional)."""
    var = variancia(dados, amostral=amostral)
    return var ** 0.5


def coef_variacao(dados: Sequence[float], amostral: bool = True) -> float:
    """
    Coeficiente de variação: desvio padrão / média.
    Retorna um valor decimal (multiplique por 100 para %).
    """
    m = media(dados)
    if m == 0:
        raise ValueError("Coeficiente de variação indefinido para média igual a zero.")
    dp = desvio_padrao(dados, amostral=amostral)
    return dp / m


# ---------------------------------------------------------------------------
# Quartis / percentis
# ---------------------------------------------------------------------------

def percentil(dados: Sequence[float], p: float) -> float:
    """
    Percentil p (0 a 100) usando interpolação linear entre os pontos mais
    próximos — mesmo método usado por padrão em numpy.percentile
    (interpolation='linear'), para permitir validação direta.
    """
    _validar_nao_vazio(dados)
    if not (0 <= p <= 100):
        raise ValueError("p deve estar entre 0 e 100.")

    ordenados = _ordenar(dados)
    n = len(ordenados)
    if n == 1:
        return float(ordenados[0])

    # posição "ideal" (0-indexada) dentro da lista ordenada
    posicao = (p / 100) * (n - 1)
    indice_inferior = int(posicao)  # trunca
    indice_superior = min(indice_inferior + 1, n - 1)
    fracao = posicao - indice_inferior

    valor = ordenados[indice_inferior] + fracao * (
        ordenados[indice_superior] - ordenados[indice_inferior]
    )
    return valor


def quartis(dados: Sequence[float]) -> Tuple[float, float, float]:
    """Retorna (Q1, Q2, Q3) usando a função de percentil acima."""
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)
    return (q1, q2, q3)


def iqr(dados: Sequence[float]) -> float:
    """Intervalo interquartil: Q3 - Q1."""
    q1, _, q3 = quartis(dados)
    return q3 - q1


# ---------------------------------------------------------------------------
# Covariância e correlação
# ---------------------------------------------------------------------------

def covariancia(x: Sequence[float], y: Sequence[float], amostral: bool = True) -> float:
    """
    Covariância entre duas variáveis. Por padrão, amostral (divide por n-1).
    """
    _validar_nao_vazio(x)
    _validar_nao_vazio(y)
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho.")

    n = len(x)
    if amostral and n < 2:
        raise ValueError("Covariância amostral requer ao menos 2 pares de valores.")

    media_x = media(x)
    media_y = media(y)

    soma = 0.0
    for xi, yi in zip(x, y):
        soma += (xi - media_x) * (yi - media_y)

    denominador = (n - 1) if amostral else n
    return soma / denominador


def correlacao_pearson(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Coeficiente de correlação de Pearson (r), entre -1 e 1.
    r = cov(x, y) / (desvio_padrao(x) * desvio_padrao(y))
    """
    cov = covariancia(x, y, amostral=True)
    dp_x = desvio_padrao(x, amostral=True)
    dp_y = desvio_padrao(y, amostral=True)

    if dp_x == 0 or dp_y == 0:
        raise ValueError("Correlação indefinida quando uma das variáveis tem desvio padrão zero.")

    return cov / (dp_x * dp_y)


# ---------------------------------------------------------------------------
# Regressão linear simples (provavelmente sera usada no Módulo 5, mas já deixamos pronta aqui)
# ---------------------------------------------------------------------------

def regressao_linear_simples(x: Sequence[float], y: Sequence[float]) -> Tuple[float, float]:
    """
    Ajusta y = a + b*x pelo método dos mínimos quadrados.
    Retorna (a, b) = (intercepto, coeficiente angular).
    """
    _validar_nao_vazio(x)
    _validar_nao_vazio(y)
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho.")

    media_x = media(x)
    media_y = media(y)

    numerador = 0.0
    denominador = 0.0
    for xi, yi in zip(x, y):
        numerador += (xi - media_x) * (yi - media_y)
        denominador += (xi - media_x) ** 2

    if denominador == 0:
        raise ValueError("Não é possível ajustar a reta: variância de x é zero.")

    b = numerador / denominador
    a = media_y - b * media_x
    return (a, b)


def r_quadrado(x: Sequence[float], y: Sequence[float]) -> float:
    """R² da regressão linear simples: quadrado do coeficiente de Pearson."""
    r = correlacao_pearson(x, y)
    return r ** 2


# ---------------------------------------------------------------------------
# Distribuições teóricas (Módulo 4)
# ---------------------------------------------------------------------------

def densidade_normal(x: float, media_dados: float, desvio_padrao_dados: float) -> float:
    """
    Densidade de probabilidade da distribuição Normal (Gaussiana) no ponto x,
    pela fórmula fechada -- não usa scipy.stats.norm:

        f(x) = (1 / (sigma * sqrt(2*pi))) * exp(-(x - mu)^2 / (2 * sigma^2))
    """
    if desvio_padrao_dados <= 0:
        raise ValueError("O desvio padrão deve ser maior que zero.")
    expoente = -((x - media_dados) ** 2) / (2 * desvio_padrao_dados ** 2)
    return (1.0 / (desvio_padrao_dados * math.sqrt(2 * math.pi))) * math.exp(expoente)


def densidade_uniforme(x: float, minimo: float, maximo: float) -> float:
    """Densidade de probabilidade da distribuição Uniforme contínua em [minimo, maximo]."""
    if maximo <= minimo:
        raise ValueError("O máximo deve ser maior que o mínimo.")
    if minimo <= x <= maximo:
        return 1.0 / (maximo - minimo)
    return 0.0


def densidade_exponencial(x: float, taxa: float) -> float:
    """
    Densidade de probabilidade da distribuição Exponencial com parâmetro de
    taxa (lambda). Definida para x >= 0; fora disso a densidade é zero.
    """
    if taxa <= 0:
        raise ValueError("A taxa (lambda) deve ser maior que zero.")
    if x < 0:
        return 0.0
    return taxa * math.exp(-taxa * x)

def assimetria(dados):
    """
    Calcula o coeficiente de assimetria (skewness) de Fisher-Pearson, manualmente, usando o terceiro momento padronizado da amostra.
    Equivalente ao scipy.stats.skew(dados, bias=True) -- usado apenas para VALIDAR o resultado no Modulo 6, nunca para calcula-lo.
    """
    n = len(dados)
    if n < 3:
        raise ValueError("São necessários pelo menos 3 valores para calcular a assimetria.")

    media_dados = media(dados)
    desvio = desvio_padrao(dados, amostral=False)  # desvio padrão populacional

    if desvio == 0:
        return 0.0

    soma_cubos = sum((x - media_dados) ** 3 for x in dados)
    return (soma_cubos / n) / (desvio ** 3)