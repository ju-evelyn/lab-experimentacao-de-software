import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv("../repos.csv")

mediana_idade_repositorios = csv['Repository Age'].median()
mediana_prs_aceitas = csv["Accepted Pull Requests"].median()
mediana_total_releases = csv["Total Releases"].median()
mediana_tempo_atualizacao = csv["Time since last update"].median()
moda_linguagem_primaria = csv["Primary Language"].mode()
mediana_razao_issues = csv["Closed Issues %"].median()

# linguagem_primaria = csv["Primary Language"]
# linguagem_primaria_ordenada = linguagem_primaria

print("Mediana da Idade dos Repositórios:", mediana_idade_repositorios)
print("Mediana das prs aceitas:", mediana_prs_aceitas)
print("Mediana do total de releases:", mediana_total_releases)
print("Mediana do tempo de atualização:", mediana_tempo_atualizacao)
print("Moda das linguagens primárias:", moda_linguagem_primaria)
print("Mediana das razões das issues:", mediana_razao_issues)

# Supondo que 'df' seja o seu DataFrame
plt.figure(figsize=(12, 8))

# Lista de colunas que você deseja plotar (por exemplo, 'StarsCount', 'RepositoryAge', etc.)
colunas = ['Repository Age', 'Accepted Pull Requests', 'Total Releases',
           'Time since last update', 'Closed Issues %']

for i, coluna in enumerate(colunas):
    plt.subplot(2, 3, i + 1)  # Cria um subplot em uma grade de 2x3
    plt.boxplot(csv[coluna], showfliers=False)  # Configuração para não mostrar outliers
    plt.title(coluna)  # Título do subplot

plt.tight_layout()
plt.show()
