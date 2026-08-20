#!/bin/bash
# Hook Automático para Claude Code
# Intercepta requisições, classifica com Karajan, seleciona modelo
# Instalado em: ~/.claude/hooks/before_submit.sh

set -euo pipefail

KARAJAN_PATH="/Users/thiago.dias/Claude_CLI/karajan"

# Extrair prompt do stdin (vem do Claude Code)
read -r prompt

# Classificar com Karajan (local, zero tokens)
classification=$(python3 "$KARAJAN_PATH/scripts/orchestrator.py" "$prompt" 2>/dev/null || echo '{"level":"balanced","model":"claude-sonnet-5"}')

# Extrair modelo
model=$(echo "$classification" | python3 -c "import sys, json; print(json.load(sys.stdin).get('model', 'claude-sonnet-5'))" 2>/dev/null || echo "claude-sonnet-5")
level=$(echo "$classification" | python3 -c "import sys, json; print(json.load(sys.stdin).get('level', 'balanced'))" 2>/dev/null || echo "balanced")

# Registrar decisão
echo "[Karajan] Modelo selecionado: $model ($level)" >&2

# Passar para Claude Code com modelo selecionado
# O Claude Code vai usar esse modelo automaticamente
export CLAUDE_MODEL="$model"

# Retornar prompt (inalterado, mas com modelo definido)
echo "$prompt"
