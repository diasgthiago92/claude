#!/bin/bash

# 📚 Index Manager - Gerenciador de Índice do Claude CLI
# Funções para gerenciar, visualizar e atualizar o índice

CLAUDE_CLI="/Users/thiago.dias/Claude_CLI"
INDEX_FILE="$CLAUDE_CLI/INDEX.md"
GENERATE_SCRIPT="$CLAUDE_CLI/scripts/generate-index.py"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==============================
# Funções
# ==============================

show_help() {
    cat << EOF
📚 Index Manager - Claude CLI

Uso: ./index-manager.sh [comando]

Comandos:
  generate   - Gerar/atualizar índice
  show       - Mostrar índice completo
  settings   - Mostrar apenas settings
  mcp        - Mostrar apenas MCP servers
  skills     - Mostrar apenas skills
  projects   - Mostrar apenas projetos
  search     - Buscar no índice (uso: search <termo>)
  stats      - Mostrar estatísticas
  watch      - Monitorar mudanças (auto-atualiza)
  help       - Esta mensagem

Exemplos:
  ./index-manager.sh generate
  ./index-manager.sh search "trix"
  ./index-manager.sh mcp
  ./index-manager.sh watch
EOF
}

# Gerar índice
generate_index() {
    echo -e "${BLUE}🔍 Gerando índice...${NC}"
    python3 "$GENERATE_SCRIPT"
    echo -e "${GREEN}✅ Índice atualizado!${NC}"
}

# Mostrar índice completo
show_index() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}📚 Mostrando INDEX.md...${NC}\n"
    less "$INDEX_FILE"
}

# Mostrar apenas settings
show_settings() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}⚙️  Settings:${NC}\n"
    sed -n '/## ⚙️/,/## 🔗/p' "$INDEX_FILE" | head -30
}

# Mostrar apenas MCP
show_mcp() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}🔗 MCP Servers:${NC}\n"
    sed -n '/## 🔗/,/## 🎯/p' "$INDEX_FILE"
}

# Mostrar skills
show_skills() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}🎯 Skills:${NC}\n"
    sed -n '/## 🎯/,/## 📁/p' "$INDEX_FILE"
}

# Mostrar projetos
show_projects() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}📁 Projetos:${NC}\n"
    sed -n '/### Projetos/,/### Memória/p' "$INDEX_FILE"
}

# Buscar no índice
search_index() {
    if [ -z "$1" ]; then
        echo -e "${YELLOW}⚠️  Use: search <termo>${NC}"
        return 1
    fi

    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}🔎 Buscando por: '$1'${NC}\n"
    grep -i "$1" "$INDEX_FILE" || echo "Nenhum resultado encontrado"
}

# Mostrar estatísticas
show_stats() {
    if [ ! -f "$INDEX_FILE" ]; then
        echo -e "${YELLOW}⚠️  Índice não existe. Gerando...${NC}"
        generate_index
    fi

    echo -e "${BLUE}📊 Estatísticas:${NC}\n"
    sed -n '/## 📊/,$p' "$INDEX_FILE" | head -20
}

# Monitorar mudanças
watch_index() {
    echo -e "${BLUE}👀 Monitorando mudanças...${NC}"
    echo -e "${YELLOW}(pressione Ctrl+C para sair)${NC}\n"

    while true; do
        clear
        echo -e "${BLUE}📚 INDEX MONITOR${NC}"
        echo "Última atualização: $(date '+%H:%M:%S')"
        echo ""

        sed -n '/## 📊/,$p' "$INDEX_FILE" | head -10

        echo ""
        echo -e "${YELLOW}Atualizando a cada 10 segundos...${NC}"
        sleep 10
        python3 "$GENERATE_SCRIPT" > /dev/null 2>&1
    done
}

# ==============================
# Main
# ==============================

case "${1:-help}" in
    generate)
        generate_index
        ;;
    show)
        show_index
        ;;
    settings)
        show_settings
        ;;
    mcp)
        show_mcp
        ;;
    skills)
        show_skills
        ;;
    projects)
        show_projects
        ;;
    search)
        search_index "$2"
        ;;
    stats)
        show_stats
        ;;
    watch)
        watch_index
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${YELLOW}Comando desconhecido: $1${NC}"
        show_help
        exit 1
        ;;
esac
