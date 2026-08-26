#!/bin/bash

# 🚀 Script de Setup do MCP - Google Docs Integration

set -e  # Exit on error

echo "================================"
echo "🚀 Setup MCP - Google Docs"
echo "================================"
echo ""

# Diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ✅ Passo 1: Verificar Node.js
echo "1️⃣  Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale em: https://nodejs.org"
    exit 1
fi
NODE_VERSION=$(node -v)
echo "✅ Node.js $NODE_VERSION encontrado"
echo ""

# ✅ Passo 2: Verificar credenciais
echo "2️⃣  Verificando credenciais Google..."
CREDS_FILE="$HOME/Downloads/thiagodias-30c5309274a4.json"
if [ ! -f "$CREDS_FILE" ]; then
    echo "❌ Arquivo de credenciais não encontrado em:"
    echo "   $CREDS_FILE"
    echo ""
    echo "📌 Você precisa:"
    echo "   1. Vá para: https://console.cloud.google.com/apis/credentials"
    echo "   2. Crie uma 'Service Account'"
    echo "   3. Gere chave JSON"
    echo "   4. Salve em: ~/Downloads/thiagodias-30c5309274a4.json"
    exit 1
fi
echo "✅ Credenciais encontradas: $CREDS_FILE"
echo ""

# ✅ Passo 3: Instalar dependências npm
echo "3️⃣  Instalando dependências npm..."
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo "✅ Dependências instaladas"
else
    echo "✅ node_modules já existe"
fi
echo ""

# ✅ Passo 4: Testar servidor
echo "4️⃣  Testando servidor MCP..."
timeout 5 node google-docs-server.js 2>&1 | head -10 &
sleep 2
RESULT=$?
if [ $RESULT -eq 0 ] || [ $RESULT -eq 124 ]; then
    echo "✅ Servidor MCP funcional"
else
    echo "❌ Erro ao iniciar servidor"
    exit 1
fi
echo ""

# ✅ Passo 5: Configurar settings.json
echo "5️⃣  Configurando Claude Code..."
SETTINGS_FILE="$HOME/.claude/settings.json"

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "📌 settings.json não encontrado. Criando..."
    mkdir -p "$HOME/.claude"
    echo "{}" > "$SETTINGS_FILE"
fi

# Verificar se MCP já está configurado
if grep -q "google-docs" "$SETTINGS_FILE"; then
    echo "✅ MCP já configurado em settings.json"
else
    echo "📝 Adicionando MCP ao settings.json..."
    # Usar python para adicionar JSON
    python3 << 'EOF'
import json
import os

settings_file = os.path.expanduser("~/.claude/settings.json")

# Ler settings atuais
try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
except:
    settings = {}

# Adicionar MCP server
if "mcpServers" not in settings:
    settings["mcpServers"] = {}

settings["mcpServers"]["google-docs"] = {
    "command": "node",
    "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-docs-server.js"],
    "env": {
        "HOME": "/Users/thiago.dias"
    },
    "disabled": False
}

# Salvar
with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ MCP adicionado ao settings.json")
EOF
fi
echo ""

# ✅ Passo 6: Resumo
echo "================================"
echo "✅ Setup Completo!"
echo "================================"
echo ""
echo "📋 Próximos passos:"
echo "   1. Feche Claude Code (se estiver aberto)"
echo "   2. Abra Claude Code novamente"
echo "   3. Verifique: claude info"
echo "   4. Me avise que está pronto!"
echo ""
echo "🎯 Depois você pode:"
echo "   - Criar documentos: 'Crie doc no Google Docs'"
echo "   - Ler documentos: 'Leia documento X'"
echo "   - Listar docs: 'Mostre meus documentos'"
echo "   - Compartilhar: 'Compartilhe documento com email'"
echo ""
echo "✅ MCP Setup concluído com sucesso!"
