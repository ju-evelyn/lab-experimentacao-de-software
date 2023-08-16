import requests
from JsonToRepositoryConverter import JsonToRepositoryConvert


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
  repositories: search(query: "stars:>100", type: REPOSITORY, first: $perPage, after: $cursor) {
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
while totalCollected < 100:
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


with open("repos.txt", "w") as arquivo:
    arquivo.write(" ")

i=0 # Contador para a ordem decrescente de Repos com mais stars
for repo in all_repositories:
    i += 1
    # Formatando as respostas para o txt
    repositoriosTXT = '''
        {} - Nome do repositório: {} | Stars: {}
        RQ 01 - idade do repositório: {}
        RQ 02 - pull requests aceitas: {}
        RQ 03 - total de releases: {}
        RQ 04 - tempo até a última atualização: {}
        RQ 05 - linguagem primária: {}
        RQ 06 - razão de issues fechadas: {}
        --------------------------------------------------------------------------
    '''.format(i, repo.getNode().getName(), repo.getNode().getStarsCount(), repo.getRepositoryAge().__str__(),
               str(repo.getNode().getMergedPRsCount().getPRsTotalCount()),
               str(repo.getNode().getRelease().getReleaseTotalCount()),
               str(repo.getTimeSinceLastUpdate()),
               repo.getNode().validatePrimaryLanguage(),
               str(repo.getClosedIssuesRatio()))

    # Adicionando as informações do repositório no txt
    with open("repos.txt", "a") as arquivo:
        arquivo.write(repositoriosTXT)
print('Objetos adicionados ao arquivo')