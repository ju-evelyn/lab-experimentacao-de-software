import datetime


class RepositoryData:
    repositoryAge = datetime
    timeSinceLastUpdate = datetime
    closedIssuesRatio = float

    def __init__(self, node):
        self.node = node
        self.repositoryAge = self.setRepositoryAge()
        self.timeSinceLastUpdate = self.setTimeSinceLastUpdate()
        self.setClosedIssuesRatio(node.getClosedIssuesCount().getIssuesCount(),
                                  node.getTotalIssuesCount().getIssuesCount())

    def setRepositoryAge(self):
        return datetime.datetime.today() - self.node.creationDate

    def setTimeSinceLastUpdate(self):
        return datetime.datetime.today() - self.node.lastUpdateDate

    def setClosedIssuesRatio(self, closedIssues, totalIssues):
        if totalIssues is not None and totalIssues != 0:
            self.closedIssuesRatio = closedIssues / totalIssues
        else:
            self.closedIssuesRatio = 0

    def getNode(self):
        return self.node

    def getRepositoryAge(self):
        return self.repositoryAge

    def getClosedIssuesRatio(self):
        return self.closedIssuesRatio

    def getTimeSinceLastUpdate(self):
        return self.timeSinceLastUpdate


class Node:
    def __init__(self, name, starsCount, creationDate, mergedPRsCount, releaseCount,
                 primaryLanguage, lastUpdateDate, totalIssuesCount, closedIssuesCount):
        self.name = name
        self.starsCount = starsCount
        self.creationDate = creationDate
        self.mergedPRsCount = mergedPRsCount
        self.releaseCount = releaseCount
        self.primaryLanguage = primaryLanguage
        self.lastUpdateDate = lastUpdateDate
        self.totalIssuesCount = totalIssuesCount
        self.closedIssuesCount = closedIssuesCount

    def getName(self):
        return self.name

    def getCreationDate(self):
        return self.creationDate

    def getMergedPRsCount(self):
        return self.mergedPRsCount

    def getTotalIssuesCount(self):
        return self.totalIssuesCount

    def getClosedIssuesCount(self):
        return self.closedIssuesCount

    def getRelease(self):
        return self.releaseCount

    def getPrimaryLanguage(self):
        return self.primaryLanguage

    def validatePrimaryLanguage(self) -> str:
        if str(self.getPrimaryLanguage()) != '':
            return str(self.getPrimaryLanguage().getPrimaryLanguageName())
        else:
            return "none"


class PullRequests:
    def __init__(self, totalCount):
        self.totalCount = totalCount

    def getPRsTotalCount(self):
        return self.totalCount


class Releases:
    def __init__(self, totalCount):
        self.totalCount = totalCount

    def getReleaseTotalCount(self):
        return self.totalCount


class PrimaryLanguage:
    def __init__(self, name='none'):
        self.name = name

    def getPrimaryLanguageName(self):
        return self.name


class Issues:
    def __init__(self, issuesCount):
        self.issuesCount = issuesCount

    def getIssuesCount(self):
        return self.issuesCount
