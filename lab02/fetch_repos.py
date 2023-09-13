import os
import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# Função para fazer a requisição GraphQL
def make_graphql_request(query, variables):
    url = 'https://api.github.com/graphql'

    # Token de acesso
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'  # Substitua pelo seu token de acesso
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response

query_template = '''
query GetRepositories($perPage: Int!, $cursor: String) {
    repositories: search(query: "stars:>10 sort:stars-desc language:Java", type: REPOSITORY, first: $perPage, after: $cursor) {
        edges {
            cursor
            node {  
                ... on Repository {
                    name
                    stargazerCount
                    url
                    createdAt
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

def fetch_1000_repos():
    perPage = 10  # Número de resultados por página
    cursor = None  # Cursor para a próxima página, começa como None para a primeira página

    all_repositories = []

    totalCollected = 0
    while totalCollected < 1000:
        variables = {
            "perPage": perPage,
            "cursor": cursor
        }

        query = query_template
        response = make_graphql_request(query, variables)

        if response.status_code != 200:
            raise Exception('Query failed to run by returning code of {}. {}'.format(response.status_code, query))

        data = response.json()['data']['repositories']
        repositories = data['edges']
        pageInfo = data['pageInfo']

        all_repositories.extend(repositories)

        totalCollected += len(repositories)
        print('Total collected: {}'.format(totalCollected))

        if pageInfo['hasNextPage']:
            cursor = pageInfo['endCursor']
        else:
            break

    all_repositories_nodes = [repo['node'] for repo in all_repositories]
    return all_repositories_nodes

def dict_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('repos.csv', index=False)
    return df


def main():
    response = fetch_1000_repos()
    return dict_to_csv(response)

if __name__ == '__main__':
    main()
