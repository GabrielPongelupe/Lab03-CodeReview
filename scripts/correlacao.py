import pandas as pd
from scipy.stats import spearmanr
import numpy as np

# Carregar CSV
df = pd.read_csv('../data/processed/prs_clean.csv')

# Preparar dados
df['status_numeric'] = df['merged'].astype(int)
df['tamanho'] = df['changed_files'] + df['additions'] + df['deletions']
df['interacoes'] = df['comments'] + df['review_comments']

print("="*80)
print("ANÁLISE DE CORRELAÇÃO DE SPEARMAN - LAB03")
print("="*80)

# RQ01
corr, p = spearmanr(df['tamanho'], df['status_numeric'])
print(f"\nRQ01 - Tamanho vs Status: ρ = {corr:.4f}, p = {p:.4f}")

# RQ02
corr, p = spearmanr(df['review_time_h'], df['status_numeric'])
print(f"RQ02 - Tempo vs Status: ρ = {corr:.4f}, p = {p:.4f}")

# RQ03
corr, p = spearmanr(df['body_length'], df['status_numeric'])
print(f"RQ03 - Descrição vs Status: ρ = {corr:.4f}, p = {p:.4f}")

# RQ04
corr, p = spearmanr(df['interacoes'], df['status_numeric'])
print(f"RQ04 - Interações vs Status: ρ = {corr:.4f}, p = {p:.4f}")

# RQ05
corr, p = spearmanr(df['tamanho'], df['review_comments'])
print(f"\nRQ05 - Tamanho vs Revisões: ρ = {corr:.4f}, p = {p:.4f}")

# RQ06
corr, p = spearmanr(df['review_time_h'], df['review_comments'])
print(f"RQ06 - Tempo vs Revisões: ρ = {corr:.4f}, p = {p:.4f}")

# RQ07
corr, p = spearmanr(df['body_length'], df['review_comments'])
print(f"RQ07 - Descrição vs Revisões: ρ = {corr:.4f}, p = {p:.4f}")

# RQ08
corr, p = spearmanr(df['interacoes'], df['review_comments'])
print(f"RQ08 - Interações vs Revisões: ρ = {corr:.4f}, p = {p:.4f}")