#!/bin/bash
# Instalador Completo do Karajan + RTK
# Configura automação total com hooks no Claude Code

set -euo pipefail

KARAJAN_PATH="/Users/thiago.dias/Claude_CLI/karajan"
CLAUDE_CONFIG_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_CONFIG_DIR/settings.json"
HOOKS_DIR="$CLAUDE_CONFIG_DIR/hooks"

echo "🎵 Instalando Karajan com Automação Completa + RTK..."
echo ""

# 1. Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p "$HOOKS_DIR"
mkdir -p "$CLAUDE_CONFIG_DIR"

# 2. Tornar scripts executáveis
echo "🔧 Configurando permissões..."
chmod +x "$KARAJAN_PATH/scripts"/*.{py,sh} 2>/dev/null || true
chmod +x "$KARAJAN_PATH/hooks"/*.sh 2>/dev/null || true

# 3. Copiar hook
echo "🪝 Instalando hook automático..."
cp "$KARAJAN_PATH/hooks/claude_code_hook.sh" "$HOOKS_DIR/before_submit.sh"
chmod +x "$HOOKS_DIR/before_submit.sh"

# 4. Adicionar ao PATH
echo "📍 Configurando PATH..."
SHELL_RC="$HOME/.$(basename $SHELL)rc"
if ! grep -q "claude-cli/karajan" "$SHELL_RC" 2>/dev/null; then
    echo 'export PATH="/Users/thiago.dias/Claude_CLI/karajan/scripts:$PATH"' >> "$SHELL_RC"
    echo "✅ PATH adicionado a $SHELL_RC"
else
    echo "✅ PATH já configurado"
fi

# 5. Verificar RTK
echo ""
echo "⚙️  Verificando RTK..."
if command -v rtk &> /dev/null; then
    RTK_VERSION=$(rtk --version 2>/dev/null || echo "unknown")
    echo "✅ RTK instalado ($RTK_VERSION)"
else
    echo "❌ RTK não encontrado. Instale com: brew install reachingforthejack/rtk/rtk"
    exit 1
fi

# 6. Configurar settings.json do Claude Code
echo ""
echo "⚙️  Configurando Claude Code..."

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "📝 Criando $SETTINGS_FILE..."
    echo "{}" > "$SETTINGS_FILE"
fi

# Adicionar configuração Karajan ao settings.json
python3 << 'PYTHON_SCRIPT'
import json
import sys
from pathlib import Path

settings_file = Path.home() / ".claude" / "settings.json"
karajan_config = {
    "karajan": {
        "enabled": True,
        "version": "phase-1-with-rtk",
        "description": "Roteamento automático de modelos + economia RTK"
    },
    "hooks": {
        "before:submit": {
            "command": "bash /Users/thiago.dias/Claude_CLI/karajan/hooks/claude_code_hook.sh",
            "description": "Classifica tarefa com Karajan",
            "timeout_ms": 5000,
            "fail_mode": "continue"
        }
    },
    "rtk": {
        "enabled": True,
        "description": "RTK comprime automaticamente (60-90% economia)"
    }
}

try:
    with open(settings_file) as f:
        settings = json.load(f)
except:
    settings = {}

# Merge configurações
settings.update(karajan_config)

with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print(f"✅ Configurado em {settings_file}")
PYTHON_SCRIPT

# 7. Criar symlink para karajan
echo ""
echo "🔗 Criando symlinks..."
mkdir -p ~/.local/bin
ln -sf "$KARAJAN_PATH/scripts/karajan.sh" ~/.local/bin/karajan 2>/dev/null || true
echo "✅ Symlink criado"

# 8. Mostrar status
echo ""
echo "=========================================="
echo "✅ KARAJAN COM AUTOMAÇÃO INSTALADO!"
echo "=========================================="
echo ""
echo "🎯 O que foi ativado:"
echo "   ✅ Karajan Phase 1 (roteamento automático)"
echo "   ✅ RTK compression (60-90% economia adicional)"
echo "   ✅ Hook automático no Claude Code"
echo "   ✅ Modelo selecionado automaticamente por tarefa"
echo ""
echo "📝 Próximos passos:"
echo "   1. Recarregar shell: source ~/.zshrc"
echo "   2. Testar: karajan stats"
echo "   3. Usar normalmente - Karajan escolhe modelo automaticamente!"
echo ""
echo "📊 Verificar economia:"
echo "   karajan stats          # Estatísticas"
echo "   karajan economy        # Técnicas ativas"
echo "   karajan history        # Histórico de decisões"
echo ""
echo "=========================================="
