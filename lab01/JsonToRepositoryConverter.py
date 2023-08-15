from RepositoryData import *
from datetime import datetime


def JsonToRepositoryConvert(data):
    repositoriesEdges = digToRepositoriesEdges(data)
    issuesEdges = digToIssuesEdges(data)

    issuesCountList = [createTotalIssuesData(item) for item in issuesEdges]
    repositories = [createRepositoryData(item) for item in repositoriesEdges]

    for i in range(len(repositories)):
        updateIssuesRatio(repositories, issuesCountList, i)

    return repositories


def digToRepositoriesEdges(data):
    dataKey = data['data']
    searchKey = dataKey['repositories']
    edgesKey = searchKey['edges']
    return edgesKey


def digToIssuesEdges(data):
    dataKey = data['data']
    searchKey = dataKey['totalIssuesCount']
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

    nodeDict = edge['node']
    nodeObj = Node(nodeDict['name'], nodeDict['stargazerCount'], formateDate(nodeDict['createdAt']), pullRequestObj,
                   releaseObj, primaryLanguageObj, formateDate(nodeDict['updatedAt']), issuesObj)

    return RepositoryData(nodeObj)


def createTotalIssuesData(edge):
    issuesDict = edge['node']['issues']
    issuesObj = Issues(issuesDict['totalCount'])

    return issuesObj


def updateIssuesRatio(repositories, issuesCounts, i):
    issuesCount = issuesCounts.__getitem__(i)
    repositories.__getitem__(i).setClosedIssuesRatio(issuesCount.getIssuesCount())


def formateDate(stringDate):
    datePattern = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(stringDate, datePattern)
