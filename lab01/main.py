import csv
import time

import requests
from JsonToRepositoryConverter import JsonToRepositoryConvert, numberLanguage

inicio = time.time()

# Função para fazer a requisição GraphQL
def make_graphql_request(query, variables):
    url = 'https://api.github.com/graphql'

    # Token de acesso
    headers = {
        'Authorization': 'Bearer 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'  # Substitua pelo seu token de acesso
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response


query_template = '''
query GetRepositories($perPage: Int!, $cursor: String) {
  repositories: search(query: "stars:>10 sort:stars-desc", type: REPOSITORY, first: $perPage, after: $cursor) {
    edges {
      cursor
      node {
        ... on Repository {
          name
          stargazerCount
          createdAt
          pullRequests(states: MERGED) {
            totalCount
          }
          releases {
            totalCount
          }
          primaryLanguage {
            name
          }
          updatedAt
          issues {
            totalCount
          }
          closed: issues(filterBy: {states: CLOSED}) {
            totalCount
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
'''

perPage = 10  # Número de resultados por página
cursor = None  # Cursor para a próxima página, começa como None para a primeira página

all_repositories = []

totalCollected = 0
while totalCollected < 1000:
    variables = {
        "perPage": perPage,
        "cursor": cursor
    }

    response = make_graphql_request(query_template, variables)

    if response.status_code == 200:
        data = response.json()
        repositories = JsonToRepositoryConvert(data)

        for repo in repositories:
            all_repositories.append(repo)
            totalCollected += 1

        pageInfo = data['data']['repositories']['pageInfo']

        if not pageInfo['hasNextPage']:
            break
        cursor = pageInfo['endCursor']
    else:
        print('Erro na requisição:', response.status_code)
        break

with open("repos.csv", "w", newline='') as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(["Repository Name", "Stars", "Repository Age", "Accepted Pull Requests", "Total Releases",
                     "Time since last update", "Primary Language", "Primary Language Number", "Closed Issues %"])

    i = 0  # Contador para a ordem decrescente de Repos com mais stars
    languageNumberList = []  # Numerando as linguagens para cálculo posterior

    for repo in all_repositories:
        i += 1
        primaryLanguage = repo.getNode().validatePrimaryLanguage()

        # Formatando as respostas para o csv
        repositoriosCSV = [
            repo.getNode().getName(),
            repo.getNode().getStarsCount(),
            repo.getRepositoryAge().__str__(),
            str(repo.getNode().getMergedPRsCount().getPRsTotalCount()),
            str(repo.getNode().getRelease().getReleaseTotalCount()),
            str(repo.getTimeSinceLastUpdate()),
            primaryLanguage,
            numberLanguage(primaryLanguage, languageNumberList),
            str(repo.getClosedIssuesRatio())
        ]

        # Adicionando as informações do repositório no csv
        writer.writerow(repositoriosCSV)

tempo_execucao = time.time() - inicio
print('Objetos adicionados ao arquivo')
print(f"Tempo de execução: {tempo_execucao} segundos")
