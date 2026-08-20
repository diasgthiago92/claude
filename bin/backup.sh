#!/bin/bash

# Backup Claude_CLI para GitHub - diasgthiago92/claude
# Executa sincronização automática diária

set -e

# Configuração
CLAUDE_CLI_PATH="/Users/thiago.dias/Claude_CLI"
GITHUB_REPO="https://github.com/diasgthiago92/claude.git"
BACKUP_TEMP_DIR="/tmp/claude-backup-$$"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_FILE="$CLAUDE_CLI_PATH/logs/backup_$(date +%Y%m%d_%H%M%S).log"

echo "[BACKUP] Iniciando sincronização às $TIMESTAMP" | tee -a "$LOG_FILE"

# Criar diretório temporário
mkdir -p "$BACKUP_TEMP_DIR"
trap "rm -rf $BACKUP_TEMP_DIR" EXIT

# Clone do repositório
echo "[BACKUP] Clonando repositório..." | tee -a "$LOG_FILE"
cd "$BACKUP_TEMP_DIR"
git clone "$GITHUB_REPO" repo 2>&1 | tee -a "$LOG_FILE"
cd repo

# Sincronizar arquivos de Claude_CLI
echo "[BACKUP] Sincronizando arquivos..." | tee -a "$LOG_FILE"
rsync -av --delete \
  --exclude '.git' \
  --exclude '.kirocrew.breadcrumb' \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude 'node_modules' \
  "$CLAUDE_CLI_PATH/" . 2>&1 | tee -a "$LOG_FILE"

# Commit e push
echo "[BACKUP] Preparando commit..." | tee -a "$LOG_FILE"
git config user.email "goncalvesdthiago@gmail.com"
git config user.name "Claude Backup"
git add -A

# Verificar se há mudanças
if git diff --cached --quiet; then
  echo "[BACKUP] Nenhuma mudança detectada" | tee -a "$LOG_FILE"
else
  COMMIT_MSG="Backup Claude_CLI - $TIMESTAMP"
  echo "[BACKUP] Fazendo commit: $COMMIT_MSG" | tee -a "$LOG_FILE"
  git commit -m "$COMMIT_MSG" 2>&1 | tee -a "$LOG_FILE"

  echo "[BACKUP] Fazendo push para GitHub..." | tee -a "$LOG_FILE"
  git push origin main 2>&1 | tee -a "$LOG_FILE"
  echo "[BACKUP] ✅ Push concluído com sucesso!" | tee -a "$LOG_FILE"
fi

echo "[BACKUP] Processo finalizado às $(date +"%Y-%m-%d %H:%M:%S")" | tee -a "$LOG_FILE"
