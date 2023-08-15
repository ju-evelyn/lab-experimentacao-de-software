import requests
from JsonToRepositoryConverter import JsonToRepositoryConvert

query = '''
{
  repositories: search(query: "stars:>100", type: REPOSITORY, first: 10) {
    edges {
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
          issues(filterBy: {states: CLOSED}) {
            totalCount
          }
        }
      }
    }
  }
  totalIssuesCount: search(query: "stars:>100", type: REPOSITORY, first: 10) {
    edges {
      node {
        ... on Repository {
          issues {
            totalCount
          }
        }
      }
    }
  }
}
'''

url = 'https://api.github.com/graphql'

# token de acesso
headers = {
    'Authorization': 'Bearer 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'
}

# requisição GraphQL
response = requests.post(url, json={'query': query}, headers=headers)


if response.status_code == 200:
    data = response.json()
    repositories = JsonToRepositoryConvert(data)

    # Limpando o arquivo TXT
    with open("repos.txt", "w") as arquivo:
        arquivo.write(" ")

    for repo in repositories:
        # Formatando as respostas para o txt
        repositoriosTXT = '''
            Nome do repositório: {}
            RQ 01 - idade do repositório: {}
            RQ 02 - pull requests aceitas: {}
            RQ 03 - total de releases: {}
            RQ 04 - tempo até a última atualização: {}
            RQ 05 - linguagem primária: {}
            RQ 06 - razão de issues fechadas: {}
            --------------------------------------------------------------------------
        '''.format(repo.getNode().getName(), repo.getRepositoryAge().__str__(),
                   str(repo.getNode().getMergedPRsCount().getPRsTotalCount()),
                   str(repo.getNode().getRelease().getReleaseTotalCount()),
                   str(repo.getTimeSinceLastUpdate()),
                   repo.getNode().validatePrimaryLanguage(),
                   str(repo.getClosedIssuesRatio()))

        # Adicionando as informações do repositório no txt
        with open("repos.txt", "a") as arquivo:
            arquivo.write(repositoriosTXT)
    print('Objetos adicionados ao arquivo')
else:
    print('Erro na requisição: ', response.status_code)
