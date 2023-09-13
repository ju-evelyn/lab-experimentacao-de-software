from fetch_repos import main as fetch_repos, get_repos
from clone_repos import main as clone_all_repos, clone_repo, delete_cloned_repo
from collect_repo_metrics import main as collect_metrics, setup_ck, run_ck

df = get_repos()

setup_ck()
for repo in df.itertuples():
    clone_repo(repo)
    run_ck(repo)
    delete_cloned_repo(repo)
