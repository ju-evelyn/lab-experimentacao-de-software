import pandas as pd

csv = pd.read_csv("../repos.csv")

mediana_idade_repositorios = csv['Repository Age'].median()
mediana_prs_aceitas = csv["Accepted Pull Requests"].median()
mediana_total_releases = csv["Total Releases"].median()
mediana_tempo_atualizacao = csv["Time since last update"].median()
mediana_linguagem_primaria = csv["Primary Language"].mode()
mediana_razao_issues = csv["Closed Issues %"].median()

# linguagem_primaria = csv["Primary Language"]
# linguagem_primaria_ordenada = linguagem_primaria

print("Mediana da Idade dos Repositórios:", mediana_idade_repositorios)
print("Mediana das prs aceitas:", mediana_prs_aceitas)
print("Mediana do total de releases:", mediana_total_releases)
print("Mediana do tempo de atualização:", mediana_tempo_atualizacao)
print("Moda das linguagens primárias:", mediana_linguagem_primaria)
print("Mediana das razões das issues:", mediana_razao_issues)
