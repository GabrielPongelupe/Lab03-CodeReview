import requests
import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def fetch_pr_details(repo_full_name, pr_number):
    """Busca detalhes completos de um PR específico"""
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"[ERRO] Falha ao buscar PR {pr_number} em {repo_full_name}: {r.json()}")
        return None
    return r.json()


def fetch_prs(repo_full_name, state="all", max_pages=2):
    """Busca PRs de um repositório"""
    prs = []
    print(f"\n[INFO] Coletando PRs de {repo_full_name}...")
    for page in range(1, max_pages+1):
        url = f"https://api.github.com/repos/{repo_full_name}/pulls?state={state}&per_page=100&page={page}"
        print(f"[INFO] Requisitando página {page} de PRs em {repo_full_name}")
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            print(f"[ERRO] {repo_full_name} - {r.json()}")
            break

        data = r.json()
        if not data:
            print(f"[INFO] Nenhum PR encontrado na página {page} de {repo_full_name}")
            break

        for i, pr in enumerate(data, start=1):
            print(f"    [DEBUG] Processando PR #{pr['number']} ({i}/{len(data)}) da página {page}")
            pr_detail = fetch_pr_details(repo_full_name, pr["number"])
            if not pr_detail:
                continue

            prs.append({
                "id": pr_detail["id"],
                "number": pr_detail["number"],
                "title": pr_detail["title"],
                "user": pr_detail["user"]["login"] if pr_detail["user"] else None,
                "created_at": pr_detail["created_at"],
                "closed_at": pr_detail["closed_at"],
                "merged_at": pr_detail["merged_at"],
                "comments": pr_detail.get("comments", 0),
                "review_comments": pr_detail.get("review_comments", 0),
                "changed_files": pr_detail.get("changed_files", 0),
                "additions": pr_detail.get("additions", 0),
                "deletions": pr_detail.get("deletions", 0),
                "state": pr_detail["state"],
                "merged": pr_detail.get("merged", False),
                "body_length": len(pr_detail["body"]) if pr_detail.get("body") else 0
            })
            # Pausa leve para evitar rate limit
            time.sleep(0.2)

        print(f"[INFO] Página {page} de {repo_full_name} concluída. PRs coletados até agora: {len(prs)}")

    print(f"[OK] Total de PRs coletados em {repo_full_name}: {len(prs)}")
    return prs


if __name__ == "__main__":
    repos = pd.read_csv("data/processed/top_repos.csv")
    all_prs = []
    for repo in tqdm(repos["full_name"].tolist()[:5], desc="Repositórios"):
        print(f"\n========== Iniciando coleta do repo: {repo} ==========")
        prs_repo = fetch_prs(repo)
        all_prs.extend(prs_repo)
        print(f"[INFO] Coleta finalizada para {repo}, total acumulado: {len(all_prs)}\n")

    df = pd.DataFrame(all_prs)
    df.to_csv("data/raw/prs_sample.csv", index=False)
    print("[OK] Arquivo salvo em data/raw/prs_sample.csv")
