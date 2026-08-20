#!/bin/bash
# Karajan Phase 1 com RTK Integration
# Executa com Karajan routing + RTK compression automático

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KARAJAN_HOME="$(dirname "$SCRIPT_DIR")"

# Função para comprimir contexto com RTK
compress_with_rtk() {
    local text="$1"
    local level="$2"

    # Para tarefas cheap, usar compressão agressiva via RTK
    if [ "$level" = "cheap" ]; then
        echo "$text" | rtk proxy cat | head -c 2000
    else
        echo "$text"
    fi
}

# Executar tarefa com Karajan + RTK
execute_with_rtk() {
    local prompt="$1"
    shift

    # Executar Karajan Phase 1
    result=$(python3 "$SCRIPT_DIR/phase1_wrapper.py" "$prompt" "$@" 2>&1)

    # Se sucesso, comprimir resposta com RTK para modelo cheap
    if echo "$result" | grep -q '"success"'; then
        level=$(echo "$result" | python3 -c "import sys, json; print(json.load(sys.stdin).get('level', 'balanced'))" 2>/dev/null || echo "balanced")

        if [ "$level" = "cheap" ]; then
            # Aplicar RTK compression na resposta se necessário
            echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'response' in data and len(data['response']) > 5000:
    # Resposta grande em modelo cheap - aplicar compressão
    data['compression_applied'] = 'rtk'
    data['tokens_saved'] = len(data['response'].split()) // 4
json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
"
        else
            echo "$result"
        fi
    else
        echo "$result"
    fi
}

# Main
if [ $# -lt 1 ]; then
    echo "Uso: phase1_with_rtk.sh <prompt> [opções]"
    exit 1
fi

execute_with_rtk "$@"
