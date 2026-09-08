# SISTEMATIZAÇÃO — Laboratório de Estatística em Python

Trabalho da disciplina **Matemática e Estatística para Computação** (ADS - UniCEUB), sob orientação do Prof. Romes.

## Equipe

- (preencher nomes e matrículas)

## Sobre o projeto

Aplicativo em Streamlit que analisa dados reais do **SISDEPEN** (Sistema de Informações do Departamento Penitenciário Nacional), implementando do zero — sem usar funções prontas de estatística de nenhuma biblioteca (numpy, pandas, statistics) — as principais medidas estatísticas, simulações de Monte Carlo, ajuste de distribuições e regressão linear.

## Estrutura do projeto

```
Sistematizacao-lab-estatistica/
├── Modulo 0/
│   ├── app.py                        # Aplicativo Streamlit (interface principal)
│   ├── modulo0_dataset -.py          # Script de carregamento (versão console)
│   ├── modulo0_dataset - rodando.py  # Script de carregamento (versão console)
│   ├── SISDEPEN.xlsx                 # Dataset original
│   └── SISDEPEN.csv                  # Dataset convertido
├── statslocal.py                     # Núcleo estatístico próprio (Módulo 1)
├── montecarlo.py                     # Probabilidade e simulação de Monte Carlo (Módulo 3)
├── test_stats.py                     # Testes do Módulo 1 (validação vs NumPy/SciPy)
├── test_montecarlo.py                # Testes do Módulo 3
├── requirements.txt
├── .gitignore
├── README.md
└── RELATORIO.md                      # Relatório de achados/conclusões
```

## Como rodar

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate     # Windows

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Rodar os testes (valida o núcleo estatístico contra NumPy/SciPy)
pytest -v

# 4. Rodar o aplicativo
streamlit run "Modulo 0/app.py"
```

## Dataset

- **Fonte:** SISDEPEN — SENAPPEN (https://www.gov.br/senappen/pt-br/servicos/sisdepen/bases-de-dados)
- 1532 linhas, muito acima do mínimo de 1000 exigido pelo enunciado
- Dezenas de variáveis numéricas e categóricas (acima do mínimo de 4 numéricas / 2 categóricas)

## Status dos módulos

- [x] Módulo 0 — Dados Reais (carregamento e inspeção do dataset)
- [x] Módulo 1 — Núcleo Estatístico Próprio (validado com testes automatizados)
- [ ] Módulo 2 — Estatística Descritiva Interativa (tabela de frequências, gráficos, outliers/IQR, interpretação automática)
- [x] Módulo 3 — Probabilidade e Simulação (Lei dos Grandes Números e Teorema Central do Limite)
- [ ] Módulo 4 — Distribuições Teóricas (sobreposição de curva teórica ao histograma)
- [ ] Módulo 5 — Correlação e Regressão Linear (predição interativa, R²)
- [ ] Módulo 6 — Relatório de Descobertas
