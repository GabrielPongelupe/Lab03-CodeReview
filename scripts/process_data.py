import pandas as pd
import os

def process_prs(file_path="data/raw/prs_sample.csv"):
    print("[INFO] Iniciando processamento do dataset bruto...")

    # Lê o CSV com os PRs brutos
    df = pd.read_csv(file_path, parse_dates=["created_at", "closed_at", "merged_at"])
    print(f"[INFO] PRs carregados: {len(df)}")

    # =============================
    # 1. Calcular tempo de análise
    # =============================
    df["end_date"] = df["merged_at"].fillna(df["closed_at"])
    df["review_time_h"] = (df["end_date"] - df["created_at"]).dt.total_seconds() / 3600

    # =============================
    # 2. Filtrar PRs válidos
    # =============================
    df = df[
        (df["review_time_h"] >= 1) &                # pelo menos 1 hora de revisão
        (df["state"].isin(["closed", "merged"])) &  # apenas PRs revisados e encerrados
        (df["reviews_count"] > 0)                   # pelo menos uma revisão
    ]

    print(f"[INFO] PRs após filtragem: {len(df)}")

    # =============================
    # 3. Selecionar métricas relevantes
    # =============================
    colunas_final = [
        "repo_full_name",
        "id",
        "number",
        "state",
        "merged",
        "created_at",
        "closed_at",
        "merged_at",
        "review_time_h",
        "changed_files",
        "additions",
        "deletions",
        "body_length",
        "participants_count",
        "reviews_count",
        "issue_comments_count",
        "inline_review_comments_count"
    ]

    # Garante que só as colunas necessárias fiquem no CSV final
    df_final = df[colunas_final].copy()

    # =============================
    # 4. Exportar dataset completo
    # =============================
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/final_dataset.csv"
    df_final.to_csv(output_path, index=False)
    print(f"[OK] Dataset final salvo em {output_path}")

    # =============================
    # 5. Mostrar resumo rápido
    # =============================
    print("\nResumo do dataset final:")
    print(df_final.describe(include='all'))


if __name__ == "__main__":
    process_prs()
