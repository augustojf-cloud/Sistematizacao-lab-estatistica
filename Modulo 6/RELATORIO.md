# Relatório de Achados — SISTEMATIZAÇÃO

## 1. Dataset escolhido
- **Nome do Grupo** Criminalística e estatística - análise estatística do sistema penitenciário e criminal
- **Integrantes do Grupo** Arthur Silas de Oliveira Costa, RA: 72601770; Augusto de Jesus Fernandes, RA:  72650179; Mateus Carvalho da Silva Vergara, RA: 72650578; Lucas Xavier Correa Rodrigues, RA: 72650473.
- **Nome:** SISDEPEN (Sistema de Informações do Departamento Penitenciário Nacional)
- **Fonte:** SENAPPEN
- **Linhas:** 1532
- **Colunas:** 1737
- **Ciclo de referência:** 19º ciclo (2025, 2º semestre)
- **Linhas duplicadas:** 0


## 2. Justificativa de escolha do dataset

A escolha do dataset foi voltada para análises de dados estatísticos do sistema prisional nacional, para trazer uma perspectiva matemática da criminalística nacional, vendo por um viés de abordagem técnico-científicas para análise de aspectos ligados à políticas públicas carcerárias no sistema nacional, correlacionando o sistema prisional ao demonstrativo geográfico regional, e subsequentemente ao demonstrativo estatístico de superpopulação carcerária em razão da densidade demográfica regional.

## 3. Estatísticas descritivas (Módulo 1)

A capacidade dos estabelecimentos para presos provisórios apresenta grande variação entre unidades: no total (masculino + feminino), a média é de aproximadamente 90,36 vagas por estabelecimento, com desvio padrão de 204,00 (evidenciando forte heterogeneidade — de unidades pequenas a grandes complexos penitenciários). O valor máximo observado chega a 1884 vagas em um único estabelecimento. Ao decompor por sexo, a capacidade masculina (média ≈ 86,36, máx. 1884) é muito superior à feminina (média ≈ 4,54, máx. 357), refletindo a proporção da população carcerária por gênero no sistema. Poderiam ser utilizados parâmetros delimitadores mais específicos para determinar uma variância maior, passível de análise, um bom exemplo pode ser a filtragem estatística para "capacidade dos estabelecimentos e sua correlação com número de presos provisórios, com um total somatizado" poderiam trazer ilustrações gráficas mais simbólicas estatisticamente falando; porém foi escolha do grupo rodar uma análise estatística mais suscinta de um dataset que é muito robusto, com uma temática muito abrangente e pode apresentar múltiplas funcionalidades desta mesma correlação exemplificada, trazendo especificadades dependendo da necessidade do usuário da aplicação. Por tais razões a limitação para uma demonstração mais objetiva e com demonstrativos estatísticos e gráficos mais métricos foi uma escolha.

## 4. Simulações de Monte Carlo (Módulo 3)

Utilizando sorteios aleatórios com reposição (semente = 42, até 1000 sorteios) sobre a coluna analisada, a Lei dos Grandes Números confirmou que a média acumulada dos valores sorteados converge para a média real da população conforme o número de sorteios aumenta. O Teorema Central do Limite foi demonstrado com amostras de tamanho n = 30: a distribuição das médias amostrais se concentra em torno da média real, aproximando-se do formato de sino esperado pela teoria.

## 5. Distribuições teóricas (Módulo 4)

O módulo permite sobrepor curvas teóricas (Normal, Uniforme, Exponencial) ao histograma de qualquer coluna numérica do dataset, possibilitando avaliar visualmente qual distribuição melhor se ajusta a cada variável.

## 6. Correlação e regressão (Módulo 5)

Analisando a relação entre CEP e Código IBGE do estabelecimento, foi obtida uma correlação fraca e positiva (r = 0,1660), com R² = 0,0276 — ou seja, o modelo explica apenas 2,8% da variação do Código IBGE a partir do CEP. A equação da reta ajustada foi: Código IBGE = 0,0074 × CEP + 2.808.621,2439.
Isso é esperado: ambas as variáveis são identificadores geográficos, não indicadores substantivos do sistema prisional, então a correlação fraca apenas reflete uma leve tendência espacial entre a numeração dos CEPs e dos códigos municipais do IBGE — não uma relação de causa e efeito.

## 7. Decisões de implementação estatística 
- Núcleo estatístico próprio (statslocal.py): todas as medidas exibidas ao
  usuário (média, mediana, moda, variância, desvio padrão, quartis/percentis,
  covariância, correlação de Pearson e regressão linear) foram implementadas
  do zero, sem usar funções prontas de estatística do NumPy/SciPy/statistics.
  NumPy/Pandas/SciPy só entram para carregar/manipular os dados e para
  validar os resultados nos testes.

- Variância e desvio padrão amostral vs. populacional: implementamos os
  dois modos (amostral=True/False), já que o trabalho pede ambos. Por
  padrão, as funções usam a versão amostral (divisão por n-1), por ser o caso
  mais comum ao trabalhar com uma amostra do sistema penitenciário em vez da
  população completa.

- Quartis/percentis por interpolação linear: a função percentil()
  usa o mesmo método de interpolação linear do numpy.percentile
  (parâmetro padrão 'interpolation='linear'), para permitir comparação
  direta e exata entre os dois nos testes automatizados.

- Detecção de outliers pela regra do IQR: no Módulo 2, outliers são
  identificados como valores fora do intervalo [Q1 - 1,5·IQR, Q3 + 1,5·IQR],
  usando os quartis calculados pela nossa própria função, não por biblioteca
  pronta.

- Simulação de Monte Carlo com média incremental (Módulo 3): para a Lei
  dos Grandes Números, em vez de recalcular a média do zero a cada novo
  sorteio (o que seria custoso para um número grande de sorteios), usamos a
  fórmula de atualização incremental média_nova = média_antiga +
  (novo_valor - média_antiga) / n, matematicamente equivalente à média
  tradicional, mas calculada progressivamente.

- Distribuições teóricas calculadas por fórmula fechada (Módulo 4): as
  densidades de probabilidade (Normal, Uniforme e Exponencial) foram
  implementadas pelas fórmulas matemáticas fechadas de cada distribuição,
  com os parâmetros estimados a partir dos próprios dados (ex.: média e
  desvio padrão da amostra para a Normal), sem usar scipy.stats.

- Tratamento de colunas sem variação (Módulo 5): algumas colunas do
  SISDEPEN são constantes em todo o dataset (ex.: ano/ciclo do
  levantamento). Como covariância/correlação exigem variação nos dados,
  essas colunas são automaticamente excluídas das opções de variável no
  módulo de correlação e regressão, evitando erro de divisão por zero.


## 8. Resultado de validação estatística
Todas as funções do núcleo estatístico (statslocal.py) foram validadas em
test_stats.py, comparando cada resultado próprio com a referência do
NumPy/SciPy, dentro de uma tolerância numérica documentada (1e-9 para
cálculos exatos, como média, variância e quartis; tolerância maior, de
1e-6, para correlação e regressão, por acumularem mais operações de ponto
flutuante).

Resultado: 17 de 17 testes automatizados passaram (100%), cobrindo:
média, mediana, moda, amplitude, variância (amostral e populacional),
desvio padrão (amostral e populacional), coeficiente de variação,
percentil, quartis, IQR, covariância, correlação de Pearson, regressão
linear simples, R², densidades de probabilidade (Normal, Uniforme,
Exponencial) e o caso de borda de lista vazia.

*(A SER PREENCHIDO: resultado da suíte de testes do Módulo 3
(`test_montecarlo.py`) — quantos testes passaram, e confirmação de que a
Lei dos Grandes Números converge para a média real da população e que o
desvio padrão das médias amostrais do Teorema Central do Limite se
aproxima do erro padrão teórico dentro da tolerância definida no código.)*



## 9. Conclusões

O dataset SISDEPEN (1532 estabelecimentos, 1737 colunas) permitiu aplicar de ponta a ponta os fundamentos de estatística descritiva, probabilidade, inferência (Monte Carlo, TCL) e regressão linear sobre dados reais do sistema penitenciário brasileiro. Os principais achados foram:

1. A superlotação dos presídios segue uma amostragem nítida em gradiente por região - a (correlação/regressão) apresentada no Módulo 5 traz a correlação de região com superlotação, demonstrando que, por exemplo, o Norte é a única regiçao com número de vagas carcerárias em superavit relativo à população carcerária; todos as outras regiões do país se encontram com superlotação carcerária; se ampliada a análise por comparativo em recorto por UF, temos uma expressividade ainda maior.

2. Os presos estrangeiros estão concentrados nas regiões fronteiriças - aqui, o recorte além de expressivo, chega a ser dicotômico e inversamente proporcional às primeiras conclusões, de modo que os percentuais apresentados chegam a mostrar o Norte com o percentual de 0,90%, mais que o dobro do segundo lugar, o Sul e Centro-Oeste, com 0,43%. A clara ocorrência da concentração carcerária está diretamente ligada à condição geográfica, um raciocínio natural em um país continental como o Brasil, principalmente em razão das condições fronteiriças com múltiplos países.

3. As visitas aos presos varia de acordo com a região e a superlotação do presídio *com dado curioso* - o percentual de visitas aos presos segue uma métrica regional de acordo com a superlotação, tendo o Sul com o maior percentual de visitas (88,5%), enquanto o Norte novamente aparece na outra ponta da métrica de visitas carcerárias (56,9%). *o aspecto curioso das estatísticas é a condição de proporcionalidade inversa para correlacionar as visitas aos presídios superlotados; o raciocínio lógico natural seria que quanto mais superlotado o presídio, menos visitas ele teria, em razão das próprias condições de degradação do sistema prisional, mas não, a proporção se mostra inversa neste aspecto, o aspecto da regionalidade, condições de locomoção para se chegar aos presídios pelos familiares dos presos e demais visitantes, as próprias condições de regionalidade de localização geográfica dos presídios trazem precariedade e falta de logísticae e viabilidade de aumento dos números de visitas, de modo que as regiões com mais infra-estrutura, que claramente abrigam maior população carcerária, trazem melhores condições de recebimento de visitas e consequentemente maior volume delas, enquanto os demais estados e regiões mais remotas, apesar de diminuir a população carcerária, também recebem menos visitas que os demais percentuais por região*

4. ***os estabelecimentos prisionais, em sua grande maioria (27 deles), declaram não abrigar condições para coletar dados de nacionalidade de presos; outros 34 relatam parcialmente estes dados relacionados à nacionalidade dos presos. Claro demonstrativo de falha do sistema prisional nacional, o que consequentemente limita também melhor demonstrativo e qualitatividade do dataset, bem como impõe-se limitações***

***Como limitação também, deve ser destacado que nem todas as colunas numéricas do dataset possuem variância para ilustrar com ampla ilustratividade variáveis de capacidade prisional poderiam ser mais ricas estatisticamente do que identificadores administrativos e regionais (ciclo, CEP, Código IBGE).*** 
