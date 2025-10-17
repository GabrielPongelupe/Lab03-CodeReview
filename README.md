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

🆕 **ATUALIZADO COM NOVOS SCRIPTS**
```bash
Lab03-CodeReview/
│── data/
│   ├── raw/              # Dados brutos coletados da API
│   │   └── prs_sample.csv
│   ├── processed/        # Dados tratados para análise
│   │   ├── top_repos.csv
│   │   └── prs_clean.csv
|   |   └── graficos.py       # 🆕 Geração de gráficos (Chart.js/HTML)   
│── scripts/              # Scripts de coleta e processamento
│   ├── fetch_repos.py    # Coleta os repositórios mais populares
│   ├── fetch_prs.py      # Coleta PRs de cada repositório
│   ├── process_data.py   # Processa e gera dataset final
│   ├── correlacao.py     # 🆕 Análise de Correlação de 
│   
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
py -m venv .venv
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

🆕 **Se der erro de `ModuleNotFoundError`, instale manualmente:**
```powershell
pip install scipy pandas numpy matplotlib seaborn
```

5. **Configure o Token do GitHub**

Crie um arquivo `.env` na raiz do projeto com o conteúdo:
```ini
GITHUB_TOKEN=seu_token_aqui
```

6. **Execute os scripts** 
```powershell
# 1. Coleta de repositórios
python scripts\fetch_repos.py

# 2. Coleta de PRs
python scripts\fetch_prs.py

# 3. Processamento e limpeza dos dados
python scripts\process_data.py

# 4. Análise de Correlação de Spearman
python scripts\correlacao.py

#gerar graficos
go live data/index.html
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

🆕 **Se der erro, instale manualmente:**
```bash
pip install scipy pandas numpy matplotlib seaborn
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

→ Gera datasets tratados em `data/processed/prs_clean.csv`.

🆕 **Análise de Correlação de Spearman:**
```bash
python scripts/correlacao.py
```

→ Gera `resultados/correlacoes.csv` com os coeficientes de correlação e p-valores.


**Visualizar Dashboard com gráficos:**

Abra `data/index.html` em um navegador ou use um servidor 




## 👨‍💻 Desenvolvido por

**Gabriel Pongelupe**  
PUC Minas - Engenharia de Software - 6º Período

**Pedro Franco**  
PUC Minas - Engenharia de Software - 6º Período