import os
from subprocess import STDOUT, check_output
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

    timeout_seconds = 60 * 5
    cmd = f'java -jar ck.jar cloned_repos/{repo.name} false 0 False ck_results/{repo.name}/'
    check_output(cmd, stderr=STDOUT, shell=True, timeout=timeout_seconds)

def generate_all_metrics():
    df = read_csv()
    for repo in df.itertuples():
        run_ck(repo)


def get_metrics_ck_from_repo(repo):
    print(repo.name)
    df_class = pd.read_csv(f'ck_results/{repo.name}/class.csv')
    df_method = pd.read_csv(f'ck_results/{repo.name}/method.csv')

    return {
        'name': repo.name,
        'CBO_median': df_class['cbo'].median(),
        'DIT_median': df_class['dit'].median(),
        'LCOM_median': df_class['lcom'].median(),
        'LOC_sum': df_method['loc'].sum(),
        'stars': repo.stargazerCount,
        'age': repo.age,
        'releases': repo.releases
    }

def get_and_append_metrics_to_df(old_df, repo):
    metrics = get_metrics_ck_from_repo(repo)
    metrics_df = pd.DataFrame([metrics])
    new_df = pd.concat([old_df, metrics_df])
    return new_df

def save_df_to_csv(df):
    df.to_csv('metrics.csv', index=False)

def df_to_csv(df):
    df.to_csv('metrics.csv', index=False)


def get_all_metrics():
    github_df = read_csv()
    metrics_df = pd.DataFrame()

    for repo in github_df.itertuples():
        metrics_df = get_and_append_metrics_to_df(metrics_df, repo)
        save_df_to_csv(metrics_df)


def main():
    setup_ck()
    generate_all_metrics()
    get_all_metrics()

if __name__ == '__main__':
    main()
