import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch_top_repos(n=200):
    print("INICIANDO FETCH, token = " + TOKEN)
    repos = []
    per_page = 100
    for page in range(1, (n // per_page) + 2):
        url = f"https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page={per_page}&page={page}"
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        repos.extend(data.get("items", []))
        print(f"[OK] Página {page} coletada")
    return repos[:n]

if __name__ == "__main__":
    repos = fetch_top_repos(200)
    df = pd.DataFrame([{
        "id": r["id"],
        "name": r["name"],
        "full_name": r["full_name"],
        "url": r["html_url"],
        "stars": r["stargazers_count"],
        "forks": r["forks_count"]
    } for r in repos])
    df.to_csv("data/processed/top_repos.csv", index=False)
    print("[OK] Arquivo salvo em data/processed/top_repos.csv")
