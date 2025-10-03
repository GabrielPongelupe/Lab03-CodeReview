# 📊 Lab03 - Code Review Analysis (Sprint 01)

## 📌 Visão Geral

Este projeto faz parte do laboratório da disciplina de **Experimentos em Engenharia de Software**.  
O objetivo é **coletar, processar e analisar Pull Requests (PRs) de repositórios populares do GitHub**, entendendo fatores que influenciam na aprovação ou rejeição dos PRs durante o processo de *code review*.  

A Sprint 01 foca em construir o **pipeline de coleta e preparação de dados**, garantindo que possamos extrair informações úteis dos PRs para análises futuras.

---

## 🎯 Objetivos da Sprint 01

- Selecionar os **200 repositórios mais populares do GitHub**.
- Coletar Pull Requests (PRs) desses repositórios.
- Processar e salvar os dados em formato estruturado (CSV).
- Montar a base inicial (`dataset`) que será usada nas próximas análises.
- Entregar um projeto organizado, reprodutível e bem documentado.

---

## 🛠️ Metodologia

1. **Coleta de Repositórios**
   - Utilizamos a API do GitHub para listar os repositórios mais populares.
   - Resultado salvo em `data/processed/top_repos.csv`.

2. **Coleta de Pull Requests**
   - Para cada repositório, coletamos PRs (merged ou closed).
   - Extraímos informações como: título, autor, número de arquivos modificados, adições, remoções, comentários e status final.
   - Resultado salvo em `data/raw/prs_sample.csv`.

3. **Processamento dos Dados**
   - Limpeza e padronização dos PRs coletados.
   - Criação de métricas como: tempo de análise, tamanho do PR, número de interações.
   - Resultado final salvo em `data/processed/`.

---

## 📂 Estrutura do Projeto

```bash
Lab03-CodeReview/
│── data/
│   ├── raw/              # Dados brutos coletados da API
│   │   └── prs_sample.csv
│   ├── processed/        # Dados tratados para análise
│   │   └── top_repos.csv
│── scripts/              # Scripts de coleta e processamento
│   ├── fetch_repos.py    # Coleta os repositórios mais populares
│   ├── fetch_prs.py      # Coleta PRs de cada repositório
│   ├── process_data.py   # Processa e gera dataset final
│── .gitignore
│── .env                  # Contém o GITHUB_TOKEN (NÃO versionar)
│── requirements.txt      # Dependências do Python
│── README.md             # Documentação do projeto
```

---
# ⚙️ Guia de Execução no Windows

### 🔹 Windows (PowerShell ou CMD)

1. **Clone o repositório**

```powershell
git clone https://github.com/seu-usuario/Lab03-CodeReview.git
cd Lab03-CodeReview
```

2. **Crie um ambiente virtual**

```powershell
python -m venv .venv
```

3. **Ative o ambiente virtual**

- No **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

- No **CMD**:

```cmd
.\.venv\Scripts\activate.bat
```

⚠️ Caso o PowerShell bloqueie a execução, execute antes (apenas na sessão atual):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. **Instale as dependências**

```powershell
pip install -r requirements.txt
```

5. **Configure o Token do GitHub**

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

```ini
GITHUB_TOKEN=seu_token_aqui
```

6. **Execute os scripts**

```powershell
python scripts\fetch_repos.py
python scripts\fetch_prs.py
python scripts\process_data.py
```



## ⚙️ Como Rodar no Linux

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Lab03-CodeReview.git
cd Lab03-CodeReview
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Token do GitHub

1. Vá em **GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens**.
2. Crie um token com permissão apenas de **leitura em repositórios públicos**.
3. Crie um arquivo `.env` na raiz do projeto:

```ini
GITHUB_TOKEN=seu_token_aqui
```

⚠️ **Importante:** O `.env` nunca deve ser commitado no GitHub (já está no `.gitignore`).

### 5. Execute os scripts

**Buscar os repositórios populares:**

```bash
python scripts/fetch_repos.py
```

→ Gera `data/processed/top_repos.csv`.

**Buscar PRs (exemplo com 5 primeiros repositórios):**

```bash
python scripts/fetch_prs.py
```

→ Gera `data/raw/prs_sample.csv`.

**Processar dados:**

```bash
python scripts/process_data.py
```

→ Gera datasets tratados em `data/processed/`.

---

## 📊 Dados Coletados (PRs)

Cada PR armazenado contém os seguintes campos principais:

| Campo | Descrição |
|-------|-----------|
| `id` | Identificador único |
| `number` | Número do PR |
| `title` | Título do PR |
| `user` | Autor |
| `created_at` | Data de criação |
| `closed_at` / `merged_at` | Datas de fechamento/merge |
| `comments` | Número de comentários |
| `review_comments` | Número de comentários de revisão |
| `changed_files` | Quantidade de arquivos alterados |
| `additions` / `deletions` | Linhas adicionadas/removidas |
| `state` | Estado final (closed / merged) |
| `merged` | Booleano se foi aceito |
| `body_length` | Tamanho da descrição do PR |

---

## ✅ Checklist da Sprint 01

- [x] `.gitignore` configurado
- [x] Ambiente virtual + dependências
- [x] Token GitHub configurado via `.env`
- [x] Script de coleta de repositórios (`fetch_repos.py`)
- [x] Script de coleta de PRs (`fetch_prs.py`)
- [x] Script de processamento (`process_data.py`)
- [x] Estrutura de pastas organizada
- [x] Documentação (README.md)

**📌 Resultado:** ao final da Sprint 01 temos um pipeline de dados completo, capaz de coletar e preparar PRs do GitHub para análises estatísticas futuras.

---

## 🚀 Próximos Passos (Sprint 02)

- Expandir coleta para todos os 200 repositórios.
- Enriquecer o dataset com informações de revisões (reviews).
- Criar hipóteses iniciais sobre fatores que influenciam no merge dos PRs.
- Primeira versão do relatório de resultados.

---

## 👨‍💻 Desenvolvido por

**Gabriel Pongelupe**  
PUC Minas - Engenharia de Software - 6º Período

**Pedro Franco**  
PUC Minas - Engenharia de Software - 6º Período

