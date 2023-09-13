import os
import pandas as pd

def read_csv():
    df = pd.read_csv('repos.csv')
    return df

def clone_repo(repo):
    print(repo.name)
    os.system(f'git clone {repo.url} cloned_repos/{repo.name}')

def delete_cloned_repo(repo):
    print(repo.name)
    os.system(f'rm -rf cloned_repos/{repo.name}')

def clone_all_repos(df):
    os.system('mkdir cloned_repos')

    for repo in df.itertuples():
        clone_repo(repo)


def main():
    df = read_csv()
    clone_all_repos(df)

if __name__ == '__main__':
    main()
    