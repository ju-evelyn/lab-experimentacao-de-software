import pandas as pd

csv = pd.read_csv("../repos.csv")

mediana_idade_repositorios = csv['Repository Age'].median()

print("Mediana da Idade dos Repositórios:", mediana_idade_repositorios)
