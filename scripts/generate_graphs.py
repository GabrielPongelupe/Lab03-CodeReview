import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os
from pathlib import Path

# Configurações de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Definir diretórios base
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / 'data' / 'processed'
RESULTS_DIR = PROJECT_DIR / 'results' / 'graphs'

# Criar diretório para os gráficos
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Carrega e prepara os dados do CSV"""
    print("Carregando dados...")
    csv_path = DATA_DIR / 'final_dataset.csv'
    
    if not csv_path.exists():
        print(f"Erro: Arquivo não encontrado em {csv_path}")
        print(f"Diretório atual: {Path.cwd()}")
        print(f"Procurando em: {csv_path.absolute()}")
        raise FileNotFoundError(f"CSV não encontrado: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Criar coluna merged (boolean)
    df['merged'] = df['merged_at'].notna()
    
    # Calcular tempo de revisão em horas
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['review_time_h'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600
    
    # Calcular total de linhas
    df['total_lines'] = df['additions'] + df['deletions']
    
    # Calcular total de interações
    df['total_interactions'] = df['comments'] + df['participants_count']
    
    print(f"Total de PRs carregados: {len(df)}")
    print(f"PRs Merged: {df['merged'].sum()}")
    print(f"PRs Closed: {(~df['merged']).sum()}")
    
    return df

def calculate_correlation(x, y, method='spearman'):
    """Calcula correlação e p-value"""
    if method == 'spearman':
        corr, p_value = stats.spearmanr(x, y)
    else:
        corr, p_value = stats.pearsonr(x, y)
    return corr, p_value

def print_statistics(merged_data, closed_data, metric_name):
    """Imprime estatísticas descritivas"""
    print(f"\n--- {metric_name} ---")
    print(f"Merged - Mediana: {merged_data.median():.2f}, Média: {merged_data.mean():.2f}")
    print(f"Closed - Mediana: {closed_data.median():.2f}, Média: {closed_data.mean():.2f}")

# ==================== DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES ====================

def rq01_tamanho_vs_status(df):
    """RQ01: Relação entre tamanho dos PRs e status final"""
    print("\n" + "="*80)
    print("RQ01: Tamanho dos PRs vs Status Final")
    print("="*80)
    
    merged = df[df['merged']]
    closed = df[~df['merged']]
    
    # Estatísticas
    print_statistics(merged['changed_files'], closed['changed_files'], 'Arquivos Modificados')
    print_statistics(merged['total_lines'], closed['total_lines'], 'Total de Linhas')
    
    # Teste estatístico (Mann-Whitney U - para dados não paramétricos)
    u_stat_files, p_value_files = stats.mannwhitneyu(merged['changed_files'], closed['changed_files'])
    u_stat_lines, p_value_lines = stats.mannwhitneyu(merged['total_lines'], closed['total_lines'])
    
    print(f"\nTeste Mann-Whitney U:")
    print(f"Arquivos - p-value: {p_value_files:.4f}")
    print(f"Linhas - p-value: {p_value_lines:.4f}")
    
    # Gráfico
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Arquivos modificados
    data_files = [merged['changed_files'], closed['changed_files']]
    bp1 = axes[0].boxplot(data_files, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp1['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    axes[0].set_ylabel('Número de Arquivos')
    axes[0].set_title('Arquivos Modificados por Status')
    axes[0].grid(True, alpha=0.3)
    
    # Total de linhas
    data_lines = [merged['total_lines'], closed['total_lines']]
    bp2 = axes[1].boxplot(data_lines, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp2['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    axes[1].set_ylabel('Total de Linhas (Adições + Remoções)')
    axes[1].set_title('Total de Linhas por Status')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'rq01_tamanho_vs_status.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {RESULTS_DIR / 'rq01_tamanho_vs_status.png'}")
    plt.close()

def rq02_tempo_vs_status(df):
    """RQ02: Relação entre tempo de análise e status final"""
    print("\n" + "="*80)
    print("RQ02: Tempo de Análise vs Status Final")
    print("="*80)
    
    merged = df[df['merged']]
    closed = df[~df['merged']]
    
    print_statistics(merged['review_time_h'], closed['review_time_h'], 'Tempo de Revisão (horas)')
    
    # Teste estatístico
    u_stat, p_value = stats.mannwhitneyu(merged['review_time_h'], closed['review_time_h'])
    print(f"\nTeste Mann-Whitney U - p-value: {p_value:.4f}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    data = [merged['review_time_h'], closed['review_time_h']]
    bp = ax.boxplot(data, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    ax.set_ylabel('Tempo de Revisão (horas)')
    ax.set_title('Tempo de Análise por Status do PR')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq02_tempo_vs_status.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq02_tempo_vs_status.png")
    plt.close()

def rq03_descricao_vs_status(df):
    """RQ03: Relação entre descrição e status final"""
    print("\n" + "="*80)
    print("RQ03: Descrição dos PRs vs Status Final")
    print("="*80)
    
    merged = df[df['merged']]
    closed = df[~df['merged']]
    
    print_statistics(merged['body_length'], closed['body_length'], 'Tamanho da Descrição (caracteres)')
    
    # Teste estatístico
    u_stat, p_value = stats.mannwhitneyu(merged['body_length'], closed['body_length'])
    print(f"\nTeste Mann-Whitney U - p-value: {p_value:.4f}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    data = [merged['body_length'], closed['body_length']]
    bp = ax.boxplot(data, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    ax.set_ylabel('Número de Caracteres na Descrição')
    ax.set_title('Tamanho da Descrição por Status do PR')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq03_descricao_vs_status.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq03_descricao_vs_status.png")
    plt.close()

def rq04_interacoes_vs_status(df):
    """RQ04: Relação entre interações e status final"""
    print("\n" + "="*80)
    print("RQ04: Interações nos PRs vs Status Final")
    print("="*80)
    
    merged = df[df['merged']]
    closed = df[~df['merged']]
    
    print_statistics(merged['participants_count'], closed['participants_count'], 'Número de Participantes')
    print_statistics(merged['comments'], closed['comments'], 'Número de Comentários')
    
    # Testes estatísticos
    u_stat_part, p_value_part = stats.mannwhitneyu(merged['participants_count'], closed['participants_count'])
    u_stat_comm, p_value_comm = stats.mannwhitneyu(merged['comments'], closed['comments'])
    
    print(f"\nTeste Mann-Whitney U:")
    print(f"Participantes - p-value: {p_value_part:.4f}")
    print(f"Comentários - p-value: {p_value_comm:.4f}")
    
    # Gráfico
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Participantes
    data_part = [merged['participants_count'], closed['participants_count']]
    bp1 = axes[0].boxplot(data_part, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp1['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    axes[0].set_ylabel('Número de Participantes')
    axes[0].set_title('Participantes por Status')
    axes[0].grid(True, alpha=0.3)
    
    # Comentários
    data_comm = [merged['comments'], closed['comments']]
    bp2 = axes[1].boxplot(data_comm, labels=['Merged', 'Closed'], patch_artist=True)
    for patch, color in zip(bp2['boxes'], ['lightgreen', 'lightcoral']):
        patch.set_facecolor(color)
    axes[1].set_ylabel('Número de Comentários')
    axes[1].set_title('Comentários por Status')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq04_interacoes_vs_status.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq04_interacoes_vs_status.png")
    plt.close()

# ==================== DIMENSÃO B: NÚMERO DE REVISÕES ====================

def rq05_tamanho_vs_revisoes(df):
    """RQ05: Relação entre tamanho e número de revisões"""
    print("\n" + "="*80)
    print("RQ05: Tamanho dos PRs vs Número de Revisões")
    print("="*80)
    
    # Correlação
    corr_files, p_files = calculate_correlation(df['changed_files'], df['review_comments'])
    corr_lines, p_lines = calculate_correlation(df['total_lines'], df['review_comments'])
    
    print(f"Correlação de Spearman:")
    print(f"Arquivos vs Revisões: ρ = {corr_files:.3f}, p-value = {p_files:.4f}")
    print(f"Linhas vs Revisões: ρ = {corr_lines:.3f}, p-value = {p_lines:.4f}")
    
    # Gráfico
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Arquivos vs Revisões
    axes[0].scatter(df['changed_files'], df['review_comments'], alpha=0.5, s=30)
    axes[0].set_xlabel('Número de Arquivos Modificados')
    axes[0].set_ylabel('Número de Review Comments')
    axes[0].set_title(f'Arquivos vs Revisões (ρ = {corr_files:.3f})')
    axes[0].grid(True, alpha=0.3)
    
    # Linhas vs Revisões
    axes[1].scatter(df['total_lines'], df['review_comments'], alpha=0.5, s=30)
    axes[1].set_xlabel('Total de Linhas (Adições + Remoções)')
    axes[1].set_ylabel('Número de Review Comments')
    axes[1].set_title(f'Linhas vs Revisões (ρ = {corr_lines:.3f})')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq05_tamanho_vs_revisoes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq05_tamanho_vs_revisoes.png")
    plt.close()

def rq06_tempo_vs_revisoes(df):
    """RQ06: Relação entre tempo de análise e número de revisões"""
    print("\n" + "="*80)
    print("RQ06: Tempo de Análise vs Número de Revisões")
    print("="*80)
    
    # Correlação
    corr, p_value = calculate_correlation(df['review_time_h'], df['review_comments'])
    print(f"Correlação de Spearman: ρ = {corr:.3f}, p-value = {p_value:.4f}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['review_time_h'], df['review_comments'], alpha=0.5, s=30)
    ax.set_xlabel('Tempo de Revisão (horas)')
    ax.set_ylabel('Número de Review Comments')
    ax.set_title(f'Tempo de Análise vs Revisões (ρ = {corr:.3f})')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq06_tempo_vs_revisoes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq06_tempo_vs_revisoes.png")
    plt.close()

def rq07_descricao_vs_revisoes(df):
    """RQ07: Relação entre descrição e número de revisões"""
    print("\n" + "="*80)
    print("RQ07: Descrição dos PRs vs Número de Revisões")
    print("="*80)
    
    # Correlação
    corr, p_value = calculate_correlation(df['body_length'], df['review_comments'])
    print(f"Correlação de Spearman: ρ = {corr:.3f}, p-value = {p_value:.4f}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['body_length'], df['review_comments'], alpha=0.5, s=30)
    ax.set_xlabel('Tamanho da Descrição (caracteres)')
    ax.set_ylabel('Número de Review Comments')
    ax.set_title(f'Descrição vs Revisões (ρ = {corr:.3f})')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq07_descricao_vs_revisoes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq07_descricao_vs_revisoes.png")
    plt.close()

def rq08_interacoes_vs_revisoes(df):
    """RQ08: Relação entre interações e número de revisões"""
    print("\n" + "="*80)
    print("RQ08: Interações nos PRs vs Número de Revisões")
    print("="*80)
    
    # Correlações
    corr_part, p_part = calculate_correlation(df['participants_count'], df['review_comments'])
    corr_comm, p_comm = calculate_correlation(df['comments'], df['review_comments'])
    
    print(f"Correlação de Spearman:")
    print(f"Participantes vs Revisões: ρ = {corr_part:.3f}, p-value = {p_part:.4f}")
    print(f"Comentários vs Revisões: ρ = {corr_comm:.3f}, p-value = {p_comm:.4f}")
    
    # Gráfico
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Participantes vs Revisões
    axes[0].scatter(df['participants_count'], df['review_comments'], alpha=0.5, s=30)
    axes[0].set_xlabel('Número de Participantes')
    axes[0].set_ylabel('Número de Review Comments')
    axes[0].set_title(f'Participantes vs Revisões (ρ = {corr_part:.3f})')
    axes[0].grid(True, alpha=0.3)
    
    # Comentários vs Revisões
    axes[1].scatter(df['comments'], df['review_comments'], alpha=0.5, s=30)
    axes[1].set_xlabel('Número de Comentários')
    axes[1].set_ylabel('Número de Review Comments')
    axes[1].set_title(f'Comentários vs Revisões (ρ = {corr_comm:.3f})')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/graphs/rq08_interacoes_vs_revisoes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: results/graphs/rq08_interacoes_vs_revisoes.png")
    plt.close()

def main():
    """Função principal"""
    print("\n" + "="*80)
    print("ANÁLISE DE CODE REVIEW - LABORATÓRIO 03")
    print("="*80)
    
    # Carregar dados
    df = load_data()
    
    # Dimensão A: Feedback Final das Revisões
    print("\n\n" + "#"*80)
    print("# DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES (STATUS DO PR)")
    print("#"*80)
    
    rq01_tamanho_vs_status(df)
    rq02_tempo_vs_status(df)
    rq03_descricao_vs_status(df)
    rq04_interacoes_vs_status(df)
    
    # Dimensão B: Número de Revisões
    print("\n\n" + "#"*80)
    print("# DIMENSÃO B: NÚMERO DE REVISÕES")
    print("#"*80)
    
    rq05_tamanho_vs_revisoes(df)
    rq06_tempo_vs_revisoes(df)
    rq07_descricao_vs_revisoes(df)
    rq08_interacoes_vs_revisoes(df)
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA!")
    print("="*80)
    print("\nTodos os gráficos foram salvos em: results/graphs/")
    print("\nResumo dos testes estatísticos:")
    print("- Dimensão A: Teste Mann-Whitney U (comparação entre grupos)")
    print("- Dimensão B: Correlação de Spearman (relação entre variáveis)")

if __name__ == "__main__":
    main()