'''python import matplotlib.pyplot as plt
import statslocal.py as ms from modulo0_dataset - rodando.py
import carregar_dataset


python import matplotlib.pyplot as plt 
import statslocal as ms from modulo0_dataset - rodando.py
import carregar_dataset (CAMINHO_ARQUIVO)

# 1. Carrega o dataset já usado no Módulo 0 df = carregar_dataset(CAMINHO_ARQUIVO) #
# 2. Troque 'coluna_x' e 'coluna_y' pelos nomes reais das colunas numéricas do seu dataset x = df['coluna_x'].tolist() y = df['coluna_y'].tolist() # 
# 3. Usa as funções já validadas pelos testes a, b = ms.regressao_linear_simples(x, y) r2 = ms.r_quadrado(x, y) print(f'Reta: y = {a:.4f} + {b:.4f}x | R² = {r2:.4f}') #
# 4. Gera o gráfico de dispersão + reta de regressão plt.scatter(x, y, label='Dados') reta_y = [a + b * xi for xi in x] plt.plot(x, reta_y, color='red', label=f'Regressão (R²={r2:.2f})') plt.xlabel('coluna_x') plt.ylabel('coluna_y') plt.legend() plt.title('Regressão Linear Simples') plt.show()#