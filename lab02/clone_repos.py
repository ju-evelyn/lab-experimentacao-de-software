import os
import pandas as pd

def read_csv():
    df = pd.read_csv('repos.csv')
    return df

def script_clone_repos(df):
    os.system('mkdir cloned_repos')

    for repo in df[:1].itertuples():
        print(repo.name)
        os.system(f'git clone {repo.url} cloned_repos/{repo.name}')


def main():
    df = read_csv()
    script_clone_repos(df)

if __name__ == '__main__':
    main()
    