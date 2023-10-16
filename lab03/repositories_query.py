import os

import pandas as pd
import requests


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
              url
              owner{
                login
              }
              pullRequests(first: 10, states: MERGED) {
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


def fetch_300_repos():
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
            data = response.json()['data']['repositories']
            repositories = data['edges']
            pageInfo = data['pageInfo']

            all_repositories.extend(repositories)

            totalCollected += len(repositories)
            print('Total collected: {}'.format(totalCollected))

            if not pageInfo['hasNextPage']:
                break
            cursor = pageInfo['endCursor']
        else:
            print('Erro na requisição:', response.status_code)
            break

    all_repositories_nodes = [repo['node'] for repo in all_repositories]
    for repo in all_repositories_nodes:
        repo['pullRequests'] = repo['pullRequests']['totalCount']
        repo['owner'] = repo['owner']['login']
    return all_repositories_nodes


def filter_repos_csv():
    repos = get_repos()
    repos = repos[repos['pullRequests'] >= 100]
    repos.to_csv('repos.csv', index=False)
    print("Repositórios com menos de 100 prs removidos")


def dict_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('repos.csv', index=False)
    return df


def get_repos():
    if os.path.exists('repos.csv'):
        return pd.read_csv('repos.csv')
    else:
        return dict_to_csv(fetch_300_repos())


def main():
    return filter_repos_csv()


if __name__ == '__main__':
    main()

