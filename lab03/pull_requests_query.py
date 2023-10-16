import os

import requests
import pandas as pd
from repositories_query import main as get_repos


def make_graphql_request(query, variables):
    url = 'https://api.github.com/graphql'

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


def fetch_prs(repos):
    perPage = 10  # Número de resultados por página
    cursor = None  # Cursor para a próxima página, começa como None para a primeira página

    all_pull_requests = []

    for repo in repos:
        repo_owner = repo['owner']
        repo_name = repo['name']
        repo_prs_total_count = int(repo['pull_requests'])
        totalCollected = 0

        while totalCollected < repo_prs_total_count:

            variables = {
                "owner": repo_owner,
                "repoName": repo_name,
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
                print('Repo: {} Total collected: {}'.format(repo_name, totalCollected))

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
    return all_pull_requests


def filter_prs_csv(prs_csv):
    filtered_prs = prs_csv[pd.to_timedelta(prs_csv['analysisTime']) >= pd.Timedelta(hours=1)]
    filtered_prs.to_csv('prs.csv', index=False)
    print("Linhas de prs com menos de uma hora de análise removidas")
    return filtered_prs


def dict_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('prs.csv', index=False)
    return df


def get_prs(repos):
    if os.path.exists('prs.csv'):
        return pd.read_csv('prs.csv')
    else:
        all_prs_dict = fetch_prs(repos)
        formatted_prs = format_all_pull_requests(all_prs_dict)
        all_prs_csv = dict_to_csv(formatted_prs)
        return filter_prs_csv(all_prs_csv)


def main():
    repos = get_repos()
    prs = get_prs(repos)
    return prs


if __name__ == '__main__':
    main()
