#!/bin/bash
# ============================================================
# Script de Instalação de Skills e Ferramentas para Claude Code
# Gerado em 2026-08-19
# ============================================================

set -e

echo "🚀 Iniciando instalação das skills para Claude Code..."
echo ""

# 1. phuryn/pm-skills
echo "📦 [1/3] Instalando PM Skills Marketplace (phuryn/pm-skills)..."
if command -v claude &> /dev/null; then
  claude plugin marketplace add phuryn/pm-skills || true
  claude plugin install pm-toolkit@pm-skills || true
  claude plugin install pm-product-strategy@pm-skills || true
  claude plugin install pm-product-discovery@pm-skills || true
  claude plugin install pm-market-research@pm-skills || true
  claude plugin install pm-data-analytics@pm-skills || true
  claude plugin install pm-marketing-growth@pm-skills || true
  claude plugin install pm-go-to-market@pm-skills || true
  claude plugin install pm-execution@pm-skills || true
  claude plugin install pm-ai-shipping@pm-skills || true
  echo "✅ PM Skills instaladas!"
else
  echo "⚠️  Claude CLI não encontrado. Instale com: npm install -g @anthropic-ai/claude-code"
fi
echo ""

# 2. JimLiu/baoyu-design
echo "🎨 [2/3] Instalando baoyu-design (Claude Design)..."
mkdir -p ~/.claude/skills
if [ -d "/tmp/baoyu-design" ]; then
  rm -rf /tmp/baoyu-design
fi
git clone --depth 1 https://github.com/JimLiu/baoyu-design.git /tmp/baoyu-design
cp -R /tmp/baoyu-design ~/.claude/skills/baoyu-design
rm -rf /tmp/baoyu-design
echo "✅ baoyu-design instalado em ~/.claude/skills/baoyu-design!"
echo ""

# 3. RefoundAI/lenny-skills
echo "📚 [3/3] Instalando lenny-skills (76 PM Skills do Lenny's Podcast)..."
if [ -d "/tmp/lenny-skills" ]; then
  rm -rf /tmp/lenny-skills
fi
git clone --depth 1 https://github.com/RefoundAI/lenny-skills.git /tmp/lenny-skills
cp -R /tmp/lenny-skills/skills/* ~/.claude/skills/
rm -rf /tmp/lenny-skills
echo "✅ lenny-skills instaladas em ~/.claude/skills/!"
echo ""

echo "============================================================"
echo "🎉 Instalação concluída!"
echo ""
echo "Skills instaladas em ~/.claude/skills/:"
ls -1 ~/.claude/skills/
echo ""
echo "💡 Para as bibliotecas de UI/Design (instalar dentro do seu projeto):"
echo "   - daisyui:       npm install daisyui"
echo "   - semi-design:   npm install @douyinfe/semi-ui"
echo "   - lucide-icons:  npm install lucide-react"
echo ""
echo "💡 Prompt Optimizer: https://prompt.always200.com"
echo "============================================================"
