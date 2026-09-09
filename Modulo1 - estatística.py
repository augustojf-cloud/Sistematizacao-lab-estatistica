# arquivo: minhastats.py
def media(lista):
    return sum(lista) / len(lista)

def variancia_amostral(lista):
    m = media(lista)
    return sum((x - m) ** 2 for x in lista) / (len(lista) - 1)