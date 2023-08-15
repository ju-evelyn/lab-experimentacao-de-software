from RepositoryData import *
from datetime import datetime


def JsonToRepositoryConvert(data):
    repositoriesEdges = digToRepositoriesEdges(data)
    repositories = [createRepositoryData(item) for item in repositoriesEdges]
    return repositories


def digToRepositoriesEdges(data):
    dataKey = data['data']
    searchKey = dataKey['repositories']
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

    issuesDict = edge['node']['issues']
    issuesObj = Issues(issuesDict['totalCount'])

    closedDict = edge['node']['closed']
    closedObj = Issues(closedDict['totalCount'])

    nodeDict = edge['node']
    nodeObj = Node(nodeDict['name'], nodeDict['stargazerCount'], formateDate(nodeDict['createdAt']), pullRequestObj,
                   releaseObj, primaryLanguageObj, formateDate(nodeDict['updatedAt']), issuesObj, closedObj)

    return RepositoryData(nodeObj)


def formateDate(stringDate):
    datePattern = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(stringDate, datePattern)
