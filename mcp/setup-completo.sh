#!/bin/bash

# 🚀 Setup Completo MCP - Google Suite Integration

set -e

echo "================================"
echo "🚀 Setup Completo MCP - Google Suite"
echo "================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar Node.js
echo "1️⃣  Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado"
    exit 1
fi
echo "✅ Node.js $(node -v) encontrado"
echo ""

# Verificar credenciais
echo "2️⃣  Verificando credenciais Google..."
CREDS_FILE="$HOME/Downloads/thiagodias-30c5309274a4.json"
if [ ! -f "$CREDS_FILE" ]; then
    echo "❌ Credenciais não encontradas: $CREDS_FILE"
    exit 1
fi
echo "✅ Credenciais encontradas"
echo ""

# Instalar dependências
echo "3️⃣  Instalando dependências npm..."
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo "✅ Dependências instaladas"
else
    echo "✅ node_modules já existe"
fi
echo ""

# Configurar settings.json
echo "4️⃣  Configurando Claude Code..."
SETTINGS_FILE="$HOME/.claude/settings.json"

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "📝 Criando settings.json..."
    mkdir -p "$HOME/.claude"
    echo "{}" > "$SETTINGS_FILE"
fi

# Adicionar todos os MCP servers
python3 << 'EOF'
import json
import os

settings_file = os.path.expanduser("~/.claude/settings.json")

try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
except:
    settings = {}

if "mcpServers" not in settings:
    settings["mcpServers"] = {}

# Google Docs
settings["mcpServers"]["google-docs"] = {
    "command": "node",
    "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-docs-server.js"],
    "disabled": False
}

# Google Slides
settings["mcpServers"]["google-slides"] = {
    "command": "node",
    "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-slides-server.js"],
    "disabled": False
}

# Google Drive
settings["mcpServers"]["google-drive"] = {
    "command": "node",
    "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-drive-server.js"],
    "disabled": False
}

# Gmail
settings["mcpServers"]["gmail"] = {
    "command": "node",
    "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-gmail-server.js"],
    "disabled": False
}

with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ Todos os MCP servers adicionados!")
print("\nServidores configurados:")
print("  • google-docs (Google Docs)")
print("  • google-slides (Google Slides/PowerPoint)")
print("  • google-drive (Google Drive)")
print("  • gmail (Gmail)")
EOF

echo ""

# Resumo
echo "================================"
echo "✅ Setup Completo!"
echo "================================"
echo ""
echo "📦 Servidores MCP instalados:"
echo "  ✅ Google Docs"
echo "  ✅ Google Slides (PowerPoint)"
echo "  ✅ Google Drive"
echo "  ✅ Gmail"
echo ""
echo "📋 Próximos passos:"
echo "  1. Feche Claude Code"
echo "  2. Abra novamente"
echo "  3. Me avise que está pronto!"
echo ""
echo "🎯 Depois você pode usar:"
echo "  • 'Crie um documento no Google'"
echo "  • 'Crie uma apresentação'"
echo "  • 'Liste meus arquivos no Drive'"
echo "  • 'Envie um email'"
echo ""
echo "✅ Setup concluído!"
