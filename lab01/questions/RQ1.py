import pandas as pd

csv = pd.read_csv("../repos.csv")

mediana_idade_repositorios = csv['Repository Age'].median()
mediana_prs_aceitas = csv["Accepted Pull Requests"].median()
mediana_total_releases = csv["Total Releases"].median()
mediana_tempo_atualizacao = csv["Time since last update"].median()
# mediana_linguagem_primaria = csv["Primary Language"].median()
mediana_razao_issues = csv["Closed Issues %"].median()

print("Mediana da Idade dos Repositórios:", mediana_idade_repositorios)
print("Mediana das prs aceitas:", mediana_prs_aceitas)
print(mediana_total_releases)
print(mediana_tempo_atualizacao)
# print(mediana_linguagem_primaria)
print(mediana_razao_issues)
