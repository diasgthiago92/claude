#!/bin/bash

# CNPJ Skill - Configuração e Setup para Claude Code
# Este script configura a skill cnpj-skill no seu ambiente

set -e

SKILL_NAME="cnpj"
SKILL_BIN="$HOME/Claude_CLI/bin/cnpj-skill"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CONFIG_DIR="$HOME/.config/cnpj-skill"

echo "🔧 Configurando CNPJ Skill..."

# Criar diretórios
mkdir -p "$CLAUDE_SKILLS_DIR" "$CONFIG_DIR"

# Verificar se o binário existe
if [[ ! -f "$SKILL_BIN" ]]; then
    echo "❌ Erro: $SKILL_BIN não encontrado"
    exit 1
fi

# Criar symlink da skill
if [[ ! -L "$CLAUDE_SKILLS_DIR/cnpj" ]]; then
    ln -s "$SKILL_BIN" "$CLAUDE_SKILLS_DIR/cnpj"
    echo "✅ Skill instalada: $CLAUDE_SKILLS_DIR/cnpj"
else
    echo "ℹ️  Skill já estava instalada"
fi

# Criar arquivo de configuração
cat > "$CONFIG_DIR/config.env" << 'EOF'
# CNPJ Skill Configuration
CACHE_ENABLED=true
CACHE_TTL=86400  # 24 horas em segundos
DEFAULT_API=brasilapi  # brasilapi ou receita

# BrasilAPI
BRASILAPI_URL=https://brasilapi.com.br/api/cnpj/v1/

# Receita Federal (opcional)
# RECEITA_DATASET_URL=...

# Logging
LOG_LEVEL=INFO
LOG_DIR=$HOME/.local/share/cnpj-skill
EOF

echo "✅ Configuração salva em: $CONFIG_DIR/config.env"

# Teste de funcionamento
echo ""
echo "🧪 Testando skill..."
if "$SKILL_BIN" --version; then
    echo "✅ Skill funcionando!"
else
    echo "⚠️  Problema na skill, verifique a instalação"
fi

echo ""
echo "📖 Para usar:"
echo "  cnpj-skill --help"
echo "  cnpj-skill --cnpj 11222333000181"
echo ""
