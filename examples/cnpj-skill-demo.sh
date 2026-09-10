#!/bin/bash

# CNPJ Skill - Demonstração de Uso
# Este script demonstra os principais recursos da skill

set -e

# Cores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       CNPJ Skill - Demonstração de Uso             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

CNPJ_VALID="11222333000181"
CNPJ_INVALID="99999999999999"

# ============================================================================
# 1. Teste de Validação
# ============================================================================

echo -e "${YELLOW}📋 1. Validando CNPJs...${NC}"
echo ""

if cnpj-skill --validate "$CNPJ_VALID" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} CNPJ válido: $CNPJ_VALID"
else
    echo "Erro na validação"
    exit 1
fi

if cnpj-skill --validate "$CNPJ_INVALID" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} CNPJ válido: $CNPJ_INVALID"
else
    echo -e "${YELLOW}!${NC} CNPJ inválido (como esperado): $CNPJ_INVALID"
fi

echo ""

# ============================================================================
# 2. Teste de Versão e Help
# ============================================================================

echo -e "${YELLOW}📖 2. Informações da Skill...${NC}"
echo ""
cnpj-skill --version
echo ""

# ============================================================================
# 3. Teste de Consulta (BrasilAPI)
# ============================================================================

echo -e "${YELLOW}🔍 3. Consultando CNPJ via BrasilAPI...${NC}"
echo ""
echo "CNPJ: $CNPJ_VALID"
echo ""

if command -v curl &> /dev/null; then
    # Fazer consulta diretamente
    echo "Resultado:"
    curl -s "https://brasilapi.com.br/api/cnpj/v1/$CNPJ_VALID" | python3 -m json.tool | head -20
    echo ""
    echo "⚠️  (resultado truncado, use 'cnpj-skill --cnpj $CNPJ_VALID' para ver tudo)"
else
    echo "curl não disponível"
fi

echo ""

# ============================================================================
# 4. Teste de Cache
# ============================================================================

echo -e "${YELLOW}💾 4. Gerenciando Cache...${NC}"
echo ""

if cnpj-skill --cache stats 2>/dev/null; then
    echo "Cache ativo"
else
    echo "Cache vazio"
fi

echo ""

# ============================================================================
# 5. Teste com Arquivo Batch (exemplo)
# ============================================================================

echo -e "${YELLOW}📑 5. Exemplo de Processamento em Lote...${NC}"
echo ""

# Criar arquivo temporário
TEMP_FILE=$(mktemp)
cat > "$TEMP_FILE" << 'EOF'
# Exemplos de CNPJs para teste
11222333000181
34028316000172
07526847000148
EOF

echo "Arquivo de entrada:"
cat "$TEMP_FILE"
echo ""
echo "Para processar este arquivo, execute:"
echo "  cnpj-skill --batch $TEMP_FILE"
echo ""

rm -f "$TEMP_FILE"

# ============================================================================
# 6. Exemplos de Uso Prático
# ============================================================================

echo -e "${YELLOW}💡 6. Exemplos de Uso Prático...${NC}"
echo ""

cat << 'EOF'
# Consulta simples
cnpj-skill --cnpj 11222333000181

# Com formatação JSON
cnpj-skill --cnpj 11222333000181 | jq '.razao_social'

# Validar CNPJ formatado
cnpj-skill --validate "11.222.333/0001-81"

# Processar lote
cnpj-skill --batch empresas.txt

# Exportar para Excel
cnpj-skill --brasilapi 11222333000181 --export dados.xlsx

# Em um loop
for cnpj in 11222333000181 34028316000172; do
    echo "Consultando: $cnpj"
    cnpj-skill --cnpj "$cnpj" | jq '.razao_social'
done

# Em Python
python3 -c "
import subprocess
import json

cnpj = '11222333000181'
result = subprocess.run(['cnpj-skill', '--cnpj', cnpj],
                       capture_output=True, text=True)
if result.returncode == 0:
    dados = json.loads(result.stdout)
    print(f'Empresa: {dados[\"razao_social\"]}')
"
EOF

echo ""

# ============================================================================
# 7. Informações Finais
# ============================================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Demonstração Concluída!               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

echo "📖 Para mais informações:"
echo "  cnpj-skill --help"
echo ""

echo "📚 Documentação completa:"
echo "  cat ~/Claude_CLI/docs/CNPJ_SKILL_README.md"
echo ""
