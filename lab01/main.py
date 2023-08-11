import requests


# Objetos da pesquisa
class RepositoryData:
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def getName(self):
        return self.node.name


class Node:
    def __init__(self, name, starsCount, creationDate, mergedPRsCount, release, primaryLanguage):
        self.name = name
        self.starsCount = starsCount
        self.creationDate = creationDate
        self.mergedPRsCount = mergedPRsCount
        self.release = release
        self.primaryLanguage = primaryLanguage


class PullRequests:
    def __init__(self, totalCount):
        self.totalCount = totalCount


class Releases:
    def __init__(self, totalCount):
        self.totalCount = totalCount


class PrimaryLanguage:
    def __init__(self, name):
        self.name = name


# Funções para transformar a resposta da query em uma lista de objetos RepositoryData
def JsonToRepositoryConvert(data):
    edges = digToTheEdges(data)
    repositories = [createRepositoryData(item) for item in edges]
    return repositories


def digToTheEdges(data):
    dataKey = data['data']
    searchKey = dataKey['search']
    edgesKey = searchKey['edges']
    return edgesKey


def createRepositoryData(edge):
    primaryLanguageObj = ''
    primaryLanguageDict = edge['node']['primaryLanguage']
    if primaryLanguageDict is not None:
        primaryLanguageObj = PrimaryLanguage(primaryLanguageDict['name'])

    releaseDict = edge['node']['releases']
    releaseObj = Releases(releaseDict["totalCount"])

    pullRequestDict = edge['node']['pullRequests']
    pullRequestObj = PullRequests(pullRequestDict['totalCount'])

    nodeDict = edge['node']
    nodeObj = Node(nodeDict['name'], nodeDict['stargazerCount'], nodeDict['createdAt'],
                   pullRequestObj, releaseObj, primaryLanguageObj)

    return RepositoryData(nodeObj)


# Query Graphql com as infos necessárias para as RQs
query = '''
query {
  search(query: "stars:>100", type: REPOSITORY, first: 10) {
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
    for repo in repositories:
        print(repo.getName())
else:
    print('Erro na requisição: ', response.status_code)
