#!/bin/bash

# 📊 Daily Token Report - Gera relatório diário de tokens

TRACKER="/Users/thiago.dias/Claude_CLI/scripts/token-tracker.py"
LOG_DIR="/Users/thiago.dias/Claude_CLI/logs/token-usage"
REPORT_DIR="/Users/thiago.dias/Claude_CLI/reports"

mkdir -p "$LOG_DIR" "$REPORT_DIR"

echo "📊 Gerando Relatório Diário de Tokens..."
echo ""

# Relatório diário
echo "=== RELATÓRIO DIÁRIO ==="
python3 "$TRACKER" daily

# Relatório semanal
echo ""
echo "=== RELATÓRIO SEMANAL ==="
python3 "$TRACKER" weekly

# Estimativa
echo ""
echo "=== ESTIMATIVA DE TOKENS ==="
python3 "$TRACKER" estimate

# Exportar para CSV
echo ""
echo "📤 Exportando para CSV..."
python3 "$TRACKER" export

echo ""
echo "✅ Relatório completo gerado!"
echo "📁 Dados em: $LOG_DIR"
echo "📊 Dashboard: open /Users/thiago.dias/Claude_CLI/scripts/token-dashboard.html"
