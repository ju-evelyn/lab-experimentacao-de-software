import pandas as pd

csv = pd.read_csv("lab01/repos.csv")

mediana_idade_repositorios = csv['Idade do Repositório'].median()

print("Mediana da Idade dos Repositórios:", mediana_idade_repositorios)
