#!/bin/bash
# Setup do Karajan - Instalar alias global

set -euo pipefail

KARAJAN_PATH="/Users/thiago.dias/Claude_CLI/karajan/scripts"
SHELL_RC="$HOME/.$(basename $SHELL)rc"

echo "🎵 Instalando Karajan..."

if grep -q "karajan" "$SHELL_RC" 2>/dev/null; then
    echo "✅ Karajan já está instalado em $SHELL_RC"
else
    echo "export PATH=\"$KARAJAN_PATH:\$PATH\"" >> "$SHELL_RC"
    echo "✅ Adicionado ao $SHELL_RC"
fi

# Criar symlink também
mkdir -p ~/.local/bin 2>/dev/null || true
ln -sf "$KARAJAN_PATH/karajan.sh" ~/.local/bin/karajan 2>/dev/null || true

echo "🎯 Recarregar shell: source $SHELL_RC"
echo "🚀 Testar: karajan help"
