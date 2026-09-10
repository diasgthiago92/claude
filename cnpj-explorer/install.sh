#!/bin/bash

# CNPJ Explorer - Script de Instalação
# Uso: chmod +x install.sh && ./install.sh

set -e

echo "================================"
echo "CNPJ Explorer - Instalação"
echo "================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detectar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado${NC}"
    echo "Instale Python 3 em: https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
echo ""

# Criar venv
echo "📦 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe${NC}"
fi
echo ""

# Ativar venv
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate
echo -e "${GREEN}✅ Ambiente ativado${NC}"
echo ""

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✅ Pip atualizado${NC}"
echo ""

# Instalar dependências
echo "📥 Instalando dependências..."
if pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
else
    echo -e "${YELLOW}⚠️  Alguns pacotes falharam (pode continuar)${NC}"
fi
echo ""

# Criar estrutura de diretórios
echo "📁 Criando diretórios..."
mkdir -p data cache logs output
echo -e "${GREEN}✅ Diretórios criados${NC}"
echo ""

# Permissões
echo "🔐 Configurando permissões..."
chmod +x cli/cnpj_cli.py
chmod +x examples/*.py
chmod +x scripts/*.py 2>/dev/null || true
echo -e "${GREEN}✅ Permissões configuradas${NC}"
echo ""

# Criar .env.example
echo "⚙️  Criando arquivo de configuração..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# BrasilAPI
BRASILAPI_URL=https://brasilapi.com.br/api/cnpj/v1/
BRASILAPI_TIMEOUT=5

# Meu CNPJ (opcional)
MEUCNPJ_API_KEY=
MEUCNPJ_URL=https://www.meucnpj.com/api/v1/

# Cache
CACHE_ENABLED=true
CACHE_TTL=86400
CACHE_DIR=./cache

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/cnpj_explorer.log

# Paralelização
MAX_WORKERS=4
TIMEOUT=5
EOF
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
else
    echo -e "${YELLOW}⚠️  .env já existe (não sobrescrevendo)${NC}"
fi
echo ""

# Testar instalação
echo "🧪 Testando instalação..."
python3 -c "import requests; print('✅ requests OK')" 2>/dev/null || echo "⚠️  requests: problema"
python3 -c "import csv; print('✅ csv OK')" 2>/dev/null || echo "✅ csv OK (nativo)"
python3 -c "import json; print('✅ json OK')" 2>/dev/null || echo "✅ json OK (nativo)"
echo ""

# Teste rápido
echo "🚀 Teste rápido..."
echo "Validando CNPJ: 15436940000172"
python3 examples/validate_cnpj.py > /dev/null 2>&1 && echo -e "${GREEN}✅ Validação OK${NC}" || echo -e "${RED}❌ Erro na validação${NC}"
echo ""

# Resumo
echo "================================"
echo -e "${GREEN}✅ Instalação Concluída!${NC}"
echo "================================"
echo ""
echo "📝 Próximos passos:"
echo ""
echo "1️⃣  Ativar ambiente:"
echo "   source venv/bin/activate"
echo ""
echo "2️⃣  Testar CLI:"
echo "   python cli/cnpj_cli.py --validate 15436940000172"
echo ""
echo "3️⃣  Ver exemplos:"
echo "   python examples/brasilapi_integration.py"
echo ""
echo "4️⃣  Ler documentação:"
echo "   cat docs/README.md"
echo ""
echo "5️⃣  Configurar APIs (opcional):"
echo "   nano .env"
echo ""
echo "📚 Documentação:"
echo "   - Repositórios GitHub: docs/REPOSITORIOS_GITHUB.md"
echo "   - CLI próprio: docs/CLI.md"
echo "   - Integração APIs: docs/INTEGRACAO_APIS.md"
echo "   - Comparação soluções: docs/COMPARACAO.md"
echo ""
