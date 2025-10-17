import pandas as pd
from scipy.stats import spearmanr
import numpy as np

# Carregar CSV final
df = pd.read_csv('data/processed/final_dataset.csv')

# Converter datas para datetime
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['closed_at'] = pd.to_datetime(df['closed_at'], errors='coerce')
df['merged_at'] = pd.to_datetime(df['merged_at'], errors='coerce')

# Calcular tempo de análise (em horas)
df['review_time_h'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600

# Converter status para variável numérica
# merged (merged_at preenchido) = 1, closed (merged_at vazio) = 0
df['status_numeric'] = df['merged_at'].notna().astype(int)

# Calcular métricas derivadas
df['tamanho'] = df['additions'] + df['deletions'] + df['changed_files']
df['interacoes'] = df['comments'] + df['review_comments']

# Remover linhas com valores ausentes
df = df.dropna(subset=['review_time_h', 'tamanho', 'body_length', 'interacoes', 'review_comments'])

print("=" * 80)
print("ANÁLISE DE CORRELAÇÃO DE SPEARMAN - LAB03")
print("=" * 80)

# Diagnóstico
print(f"\nDistribuição de status:")
print(f"Merged: {df['status_numeric'].sum()}")
print(f"Closed (não merged): {(df['status_numeric'] == 0).sum()}")
print(f"Total de PRs analisados: {len(df)}")

# Função auxiliar
def calc_corr(x, y, label):
    corr, p = spearmanr(x, y)
    print(f"{label}: ρ = {corr:.4f}, p = {p:.4f}")

# --- Relações com o Status do PR (merged ou closed)
print("\n--- Relações com o STATUS (Merged/Closed) ---")
calc_corr(df['tamanho'], df['status_numeric'], "RQ01 - Tamanho vs Status")
calc_corr(df['review_time_h'], df['status_numeric'], "RQ02 - Tempo vs Status")
calc_corr(df['body_length'], df['status_numeric'], "RQ03 - Descrição vs Status")
calc_corr(df['interacoes'], df['status_numeric'], "RQ04 - Interações vs Status")

# --- Relações com o número de revisões (review_comments)
print("\n--- Relações com o NÚMERO DE REVISÕES ---")
calc_corr(df['tamanho'], df['review_comments'], "RQ05 - Tamanho vs Revisões")
calc_corr(df['review_time_h'], df['review_comments'], "RQ06 - Tempo vs Revisões")
calc_corr(df['body_length'], df['review_comments'], "RQ07 - Descrição vs Revisões")
calc_corr(df['interacoes'], df['review_comments'], "RQ08 - Interações vs Revisões")

print("\n[OK] Análise de correlação concluída com sucesso!")