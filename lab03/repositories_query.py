import os
from itertools import cycle
import pandas as pd
import requests


tokens = ['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', 'token2', 'token3']


def make_graphql_request(query, variables, token):
    url = 'https://api.github.com/graphql'

    headers = {
        'Authorization': f'Bearer {token}'
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
              pullRequests(states: [MERGED, CLOSED]) {
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
    token_iterator = cycle(tokens)

    totalCollected = 0
    for _ in range(0, 300, 20):

        current_token = next(token_iterator)

        variables = {
            "perPage": perPage,
            "cursor": cursor
        }

        response = make_graphql_request(query_template, variables, current_token)

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


def filter_repos_csv(repos):
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
    repositories = get_repos()
    return filter_repos_csv(repositories)


if __name__ == '__main__':
    main()
