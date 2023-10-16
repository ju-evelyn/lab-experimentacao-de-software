import os

import requests
import pandas as pd
from repositories_query import main as get_repos


def make_graphql_request(query, variables):
    url = 'https://api.github.com/graphql'

    # Token de acesso
    headers = {
        'Authorization': 'Bearer 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'  # Substitua pelo seu token de acesso
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response


query_template = '''
query GetPullRequests($owner: String!, $repoName: String!, $perPage: Int!, $cursor: String) {
    repository(owner: $owner, name: $repoName) {
        pullRequests(states: [MERGED, CLOSED], first: $perPage, after: $cursor) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            title
            number
            additions
            deletions
            changedFiles
            body
            comments{
              totalCount
            }
            participants{
              totalCount
            }
            createdAt
            closedAt
            mergedAt
          }
        }
  }
}

'''


def fetch_prs(repo_owner, repo_name, repo_prs_total_count):
    perPage = 10  # Número de resultados por página
    cursor = None  # Cursor para a próxima página, começa como None para a primeira página
    owner = repo_owner
    repoName = repo_name

    all_pull_requests = []

    totalCollected = 0
    while totalCollected < repo_prs_total_count:
        variables = {
            "owner": owner,
            "repoName": repoName,
            "perPage": perPage,
            "cursor": cursor
        }

        response = make_graphql_request(query_template, variables)

        if response.status_code == 200:
            data = response.json()['data']['repository']['pullRequests']
            pull_requests = data['nodes']
            pageInfo = data['pageInfo']

            all_pull_requests.extend(pull_requests)

            totalCollected += len(pull_requests)
            print('Total collected: {}'.format(totalCollected))

            if not pageInfo['hasNextPage']:
                break
            cursor = pageInfo['endCursor']
        else:
            print('Erro na requisição:', response.status_code)
            break
    return all_pull_requests


def format_all_pull_requests(all_pull_requests):
    for repo in all_pull_requests:
        repo['comments'] = repo['comments']['totalCount']
        repo['participants'] = repo['participants']['totalCount']
        repo['bodyCharNumber'] = len(repo['body'])
        created_at = pd.Timestamp(repo['createdAt'])
        if repo['mergedAt'] is not None:
            merged_at = pd.Timestamp(repo['mergedAt'])
            repo['analysisTime'] = merged_at - created_at
        else:
            closed_at = pd.Timestamp(repo['closedAt'])
            repo['analysisTime'] = closed_at - created_at


def filter_prs_csv():
    prs = get_prs()
    format_all_pull_requests(prs)
    prs = prs[pd.to_timedelta(prs['analysisTime']) >= pd.Timedelta(hours=1)]
    prs.to_csv('prs.csv', index=False)
    print("Linhas de prs com menos de uma hora de análise removidas")


def dict_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('prs.csv', index=False)
    return df


# TODO: corrigir o método get_prs
def get_prs():
    if os.path.exists('prs.csv'):
        return pd.read_csv('prs.csv')
    else:
        return dict_to_csv(fetch_prs())


def main():
    repos = get_repos()
    all_pull_requests = []
    for repo in repos:
        repo_owner = repo['owner']
        repo_name = repo['name']
        repo_prs_total_count = repo['pull_requests']
        repo_prs_list = fetch_prs(repo_owner, repo_name, repo_prs_total_count)
        all_pull_requests.append(filter_prs_csv())

    return filter_prs_csv()


if __name__ == '__main__':
    main()
