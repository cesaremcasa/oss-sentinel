#!/bin/bash

echo "========================================="
echo "Iniciando Backup Local do OSS Sentinel"
echo "========================================="

# 1. Organização de Assets
echo ">> Organizando assets de imagem e relatórios..."
mkdir -p assets/plots
mkdir -p assets/reports

# Mover plots se a pasta de origem existir
if [ -d "data/analysis/plots" ]; then
    # O '2>/dev/null' suprime erros se não houver arquivos png para mover
    mv data/analysis/plots/*.png assets/plots/ 2>/dev/null
    echo "   [OK] Plots movidos para assets/plots/"
else
    echo "   [SKIP] Pasta data/analysis/plots não encontrada."
fi

# 2. Segurança (.gitignore)
echo ">> Verificando e atualizando .gitignore..."
GITIGNORE_FILE=".gitignore"

# Entradas obrigatórias
ENTRIES=("data/" ".env" "__pycache__/" "*.pyc" "venv/")

# Cria arquivo se não existir
if [ ! -f "$GITIGNORE_FILE" ]; then
    touch "$GITIGNORE_FILE"
fi

# Adiciona entradas que faltam
for entry in "${ENTRIES[@]}"; do
    if ! grep -q "^$entry" "$GITIGNORE_FILE"; then
        echo "$entry" >> "$GITIGNORE_FILE"
        echo "   [ADICIONADO] $entry ao .gitignore"
    fi
done
echo "   [OK] Segurança do repositório verificada."

# 3. Git Commit
echo ">> Preparando commit Git..."

# Inicializa repo se não houver (safety check)
if [ ! -d ".git" ]; then
    git init
    echo "   [INIT] Repositório Git inicializado."
fi

git add .

git commit -m "feat: MVP implementation of OSS Sentinel

- Implements ingestion layer (PyGithub)
- Implements processing layer (Pandas)
- Implements AI enrichment layer (OpenAI gpt-4o-mini)
- Implements deep diagnostic analytics (Pain Index, Heatmaps)
- Refactors output assets to /assets folder"

echo "========================================="
echo "Backup concluído com sucesso."
echo "========================================="

# 4. Log do último commit
echo ""
echo "Detalhes do Commit:"
git log -1 --stat
