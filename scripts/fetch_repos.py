import requests
import os
import pandas as pd
from dotenv import load_dotenv

# ============================================================
# Script para coletar os repositórios mais populares do GitHub
# ============================================================

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}


def fetch_top_repos(n=200):
    """
    Coleta os repositórios mais populares do GitHub com base no número de estrelas.

    Parâmetros
    ----------
    n : int
        Quantidade total de repositórios a serem coletados (padrão: 200).

    Retorno
    -------
    list
        Lista de dicionários contendo os dados dos repositórios.
    """
    print("=" * 60)
    print(" INICIANDO FETCH DE REPOSITÓRIOS POPULARES ")
    print("=" * 60)
    print(f"Token carregado: {'SIM' if TOKEN else 'NÃO'}")

    repos = []
    per_page = 100  # limite máximo da API do GitHub por página

    # Loop pelas páginas necessárias para atingir o total "n"
    for page in range(1, (n // per_page) + 2):
        url = (
            f"https://api.github.com/search/repositories"
            f"?q=stars:>1000&sort=stars&order=desc&per_page={per_page}&page={page}"
        )

        print(f"\n[REQUEST] Coletando página {page}...")
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        # Adiciona os repositórios encontrados à lista principal
        batch = data.get("items", [])
        repos.extend(batch)

        print(f"[OK] Página {page} coletada. Total acumulado: {len(repos)}")

    print(f"\n[FINALIZADO] Total de {len(repos[:n])} repositórios coletados.\n")
    return repos[:n]


if __name__ == "__main__":
    # Executa a coleta dos repositórios
    repos = fetch_top_repos(200)

    # Criação de DataFrame pandas para organizar os dados
    df = pd.DataFrame(
        [
            {
                "id": r["id"],
                "name": r["name"],
                "full_name": r["full_name"],
                "url": r["html_url"],
                "stars": r["stargazers_count"],
                "forks": r["forks_count"],
            }
            for r in repos
        ]
    )

    # Salva o resultado em CSV
    output_path = "data/processed/top_repos.csv"
    df.to_csv(output_path, index=False)

    print("[OK] Arquivo salvo em", output_path)
    print("=" * 60)
    print(" Pipeline de coleta concluído com sucesso ✅ ")
    print("=" * 60)
