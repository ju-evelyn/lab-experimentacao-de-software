import pandas as pd
import os

from fetch_repos import main as fetch_repos, get_repos
from clone_repos import main as clone_all_repos, clone_repo, delete_cloned_repo
from collect_repo_metrics import main as collect_metrics, setup_ck, run_ck, get_and_append_metrics_to_df, save_df_to_csv


github_df = get_repos()

setup_ck()

if os.path.exists('metrics.csv'):
    metrics_df = pd.read_csv('metrics.csv')
else:
    metrics_df = pd.DataFrame()

for repo in github_df.itertuples():
    clone_repo(repo)

    run_ck(repo)
    metrics_df = get_and_append_metrics_to_df(metrics_df, repo)
    save_df_to_csv(metrics_df)

    delete_cloned_repo(repo)
