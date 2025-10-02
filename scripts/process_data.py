import pandas as pd

def process_prs(file_path="data/raw/prs_sample.csv"):
    df = pd.read_csv(file_path, parse_dates=["created_at","closed_at","merged_at"])
    
    # Tempo de análise (em horas)
    df["end_date"] = df["merged_at"].fillna(df["closed_at"])
    df["review_time_h"] = (df["end_date"] - df["created_at"]).dt.total_seconds() / 3600
    
    # Filtrar PRs válidos
    df = df[
        (df["review_time_h"] >= 1) &
        (df["state"].isin(["closed"]))  
    ]
    
    df.to_csv("data/processed/prs_clean.csv", index=False)
    print("[OK] Dataset final salvo em data/processed/prs_clean.csv")

if __name__ == "__main__":
    process_prs()
