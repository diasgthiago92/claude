#!/bin/bash
# Karajan - Maestro do Roteamento de Modelos com Economia de Tokens
# Uso: karajan "<prompt>" [opções]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KARAJAN_HOME="$(dirname "$SCRIPT_DIR")"

# Funções auxiliares
show_help() {
    cat << EOF
🎵 Karajan - Orquestrador Inteligente com Economia de Tokens

FASE 1 - Execução Automática (Novo):
  karajan exec "<prompt>"               # Executa tarefa automaticamente com modelo certo
  karajan exec "<prompt>" --context-file <arquivo>   # Executa com contexto
  karajan exec "<prompt>" --force-level cheap|balanced|powerful   # Força nível

MODO CLÁSSICO - Análise:
  karajan "<prompt>"                    # Classificar tarefa e obter modelo
  karajan classify "<prompt>"           # Apenas classificar (cheap/balanced/powerful)

ECONOMIA DE TOKENS:
  karajan economy                       # Mostrar técnicas de economia ativas
  karajan economy report                # Relatório detalhado de economia
  karajan compression <level>           # Ver estratégia de compressão

MONITORAMENTO:
  karajan stats                         # Estatísticas de economia
  karajan history [N]                   # Últimas N decisões (padrão: 10)

CONFIGURAÇÃO:
  karajan config show                   # Ver configuração de economia
  karajan config edit                   # Editar configuração

Exemplos:
  karajan exec "Explica esse código"                          # Executa (Haiku)
  karajan exec "Redesenha autenticação" --force-level powerful # Força Opus
  karajan stats                                               # Ver economia
  karajan economy report                                      # Relatório detalhado

EOF
}

# Chamar o orquestrador Python
run_orchestrator() {
    python3 "$SCRIPT_DIR/orchestrator.py" "$@"
}

# Mostrar estatísticas
show_stats() {
    python3 -c "
import json
from pathlib import Path
stats_file = Path('$KARAJAN_HOME/logs/stats.json')
history_file = Path('$KARAJAN_HOME/logs/history.jsonl')

if not stats_file.exists():
    print('📊 Nenhuma estatística registrada ainda')
    exit(0)

with open(stats_file) as f:
    stats = json.load(f)

print('\n📊 Estatísticas de Economia do Karajan:')
print('=' * 50)
print(f'  Haiku 4.5 (cheap):    {stats.get(\"cheap\", 0):>3} tarefas')
print(f'  Sonnet 5 (balanced):  {stats.get(\"balanced\", 0):>3} tarefas')
print(f'  Opus 5 (powerful):    {stats.get(\"powerful\", 0):>3} tarefas')
print('=' * 50)

total = sum(stats.values())
weights = {'cheap': 1, 'balanced': 5, 'powerful': 10}
baseline = total * weights['powerful']
actual = sum(stats.get(k, 0) * weights[k] for k in weights)
savings = ((baseline - actual) / baseline * 100) if baseline > 0 else 0

print(f'\n✨ Economia estimada: ~{savings:.0f}% de tokens')
print(f'🎯 Total de tarefas roteadas: {total}')
print()
"
}

# Mostrar histórico
show_history() {
    local n=${1:-10}
    history_file="$KARAJAN_HOME/logs/history.jsonl"

    if [ ! -f "$history_file" ]; then
        echo "📜 Nenhum histórico registrado ainda"
        return
    fi

    echo "📜 Últimas $n decisões:"
    echo "================================"
    tail -n "$n" "$history_file" | python3 -c "
import sys
import json
for i, line in enumerate(sys.stdin, 1):
    data = json.loads(line)
    print(f\"{i}. [{data['decision']['level']:>8}] {data['prompt_preview']}\")
" || true
    echo
}

# Executar com Phase 1 (automático + economia)
run_phase1() {
    python3 "$SCRIPT_DIR/phase1_wrapper.py" "$@"
}

# Mostrar configuração de economia
show_economy_config() {
    cat "$KARAJAN_HOME/config/economy.json" | python3 -m json.tool
}

# Mostrar resumo de economia
show_economy_summary() {
    python3 -c "
import json
from pathlib import Path

config_file = Path('$KARAJAN_HOME/config/economy.json')
if config_file.exists():
    with open(config_file) as f:
        config = json.load(f)

    print('\n💰 Estratégias de Economia Ativas:')
    print('=' * 60)
    for technique, details in config['techniques'].items():
        if details.get('enabled'):
            print(f'\n✅ {technique.upper()}')
            print(f'   📝 {details[\"description\"]}')
            print(f'   💡 Economia: {details[\"savings_potential\"]}')
    print('\n' + '=' * 60)
else:
    print('❌ Arquivo de economia não encontrado')
"
}

# Executar com relatório de economia
show_economy_report() {
    run_phase1 --report
}

# Main
case "${1:-help}" in
    help)
        show_help
        ;;
    exec)
        if [ $# -lt 2 ]; then
            echo "Erro: prompt é necessário"
            echo "Uso: karajan exec \"<prompt>\" [opções]"
            exit 1
        fi
        run_phase1 "${@:2}"
        ;;
    stats)
        show_stats
        ;;
    history)
        show_history "${2:-10}"
        ;;
    classify)
        if [ $# -lt 2 ]; then
            echo "Erro: prompt é necessário"
            echo "Uso: karajan classify \"<prompt>\""
            exit 1
        fi
        run_orchestrator "$2" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"🎯 Nível: {data['level'].upper()}\\n📌 Modelo: {data['model']}\\n💡 Razão: {data['reason']}\")"
        ;;
    economy)
        case "${2:-help}" in
            report)
                show_economy_report
                ;;
            *)
                show_economy_summary
                ;;
        esac
        ;;
    compression)
        if [ $# -lt 2 ]; then
            echo "Erro: nível é necessário (cheap|balanced|powerful)"
            exit 1
        fi
        python3 -c "
import json
from pathlib import Path

config_file = Path('$KARAJAN_HOME/config/economy.json')
with open(config_file) as f:
    config = json.load(f)

level = '$2'
strategy = config['strategies'].get(level)
if strategy:
    print(f'\n🎯 Estratégia de Compressão para {level.upper()}')
    print('=' * 50)
    for key, value in strategy.items():
        print(f'{key:.<40} {value}')
else:
    print('❌ Nível inválido')
"
        ;;
    config)
        case "${2:-show}" in
            show)
                show_economy_config
                ;;
            edit)
                \${EDITOR:-nano} "$KARAJAN_HOME/config/economy.json"
                ;;
            *)
                show_economy_config
                ;;
        esac
        ;;
    monitor|report)
        # Mostrar relatório mensal
        python3 "$SCRIPT_DIR/monitor.py" monthly
        ;;
    report-today)
        python3 "$SCRIPT_DIR/monitor.py" today
        ;;
    report-weekly)
        weeks_back=${2:-0}
        python3 "$SCRIPT_DIR/monitor.py" weekly "$weeks_back"
        ;;
    report-all-time)
        python3 "$SCRIPT_DIR/monitor.py" all-time
        ;;
    *)
        if [ $# -lt 1 ]; then
            show_help
            exit 1
        fi
        run_orchestrator "$@"
        ;;
esac
