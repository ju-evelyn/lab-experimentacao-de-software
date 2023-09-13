import os
import pandas as pd

def download_tool_ck():
    ck_url = 'https://github.com/mauricioaniche/ck'
    os.system(f'git clone {ck_url} ck')
    os.system('rm -rf ck/.git')

def compile_ck():
    os.system('cd ck && mvn clean compile package -DskipTests')

def copy_ck_bin():
    os.system('cp ./ck/target/ck-*-SNAPSHOT-jar-with-dependencies.jar ck.jar')

def is_ck_jar_setup():
    return os.path.exists('ck.jar')

def setup_ck():
    if not is_ck_jar_setup():
        download_tool_ck()
        compile_ck()
        copy_ck_bin()


def read_csv():
    df = pd.read_csv('repos.csv')
    return df

def run_ck(repo):
    print(repo.name)
    os.system(f'mkdir -p ck_results/{repo.name}')
    os.system(f'java -jar ck.jar cloned_repos/{repo.name} false 0 False ck_results/{repo.name}/')

def collect_all_metrics():
    df = read_csv()
    for repo in df.itertuples():
        run_ck(repo)


def main():
    setup_ck()
    collect_all_metrics()

if __name__ == '__main__':
    main()
