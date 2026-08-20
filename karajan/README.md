# 🎵 Karajan - Orquestrador Inteligente de Modelos

Maestro automático que roteia suas tarefas para o modelo Claude mais eficiente, economizando tokens sem comprometer qualidade.

## 🎯 Objetivo

- **Haiku 4.5** → Tarefas simples (economia máxima)
- **Sonnet 5** → Tarefas médias (equilíbrio)
- **Opus 5** → Tarefas complexas (máxima precisão)

Economiza ~70-80% de tokens mantendo qualidade onde importa.

## 📦 Instalação

```bash
# 1. Criar alias global (add ao ~/.zshrc ou ~/.bashrc)
echo 'export PATH="/Users/thiago.dias/Claude_CLI/karajan/scripts:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 2. Testar
karajan help
```

## 🚀 Uso

### Classificar uma tarefa
```bash
karajan "Explica esse código"
```

Output:
```json
{
  "level": "cheap",
  "model": "claude-haiku-4-5-20251001",
  "reason": "Tarefa simples - usando Haiku 4.5 para economia máxima",
  "token_weight": 1
}
```

### Ver formato legível
```bash
karajan classify "Por que essa função quebrou?"
```

### Estatísticas de economia
```bash
karajan stats
```

Mostra:
- Distribuição de tarefas por modelo
- Economia percentual estimada
- Total de tarefas roteadas

### Histórico de decisões
```bash
karajan history 10  # Últimas 10 decisões
```

## 🔧 Configuração

Editar `/Users/thiago.dias/Claude_CLI/karajan/config/routes.json`:

- **classification_rules**: Palavras-chave que indicam nível
- **context_thresholds**: Limites de tamanho de contexto
- **token_weights**: Peso relativo de custo
- **fallback_strategy**: Comportamento em falhas

## 📊 Estrutura

```
karajan/
├── config/
│   └── routes.json          # Configuração de roteamento
├── logs/
│   ├── stats.json           # Estatísticas acumuladas
│   └── history.jsonl        # Histórico de decisões
├── scripts/
│   ├── orchestrator.py      # Motor de classificação
│   └── karajan.sh           # CLI wrapper
└── README.md
```

## 💡 Exemplos de Tarefas

### Cheap (Haiku 4.5)
```bash
karajan "Traduz isso para português"
karajan "Explica o que faz essa linha"
karajan "Formata esse JSON"
```

### Balanced (Sonnet 5)
```bash
karajan "Debug: essa função retorna null"
karajan "Refatora esse código para ser mais simples"
karajan "Implementa validação de input"
```

### Powerful (Opus 5)
```bash
karajan "Redesenha a arquitetura de autenticação"
karajan "Faz uma revisão de segurança completa"
karajan "Estratégia de otimização de performance"
```

## 🎭 Integração com Claude Code (Próximo)

Próximos passos:
- [ ] Hook automático para classificar tarefas antes de executar
- [ ] Seleção automática de modelo no /fast
- [ ] Dashboard de economia em tempo real
- [ ] Fallback inteligente (retry com modelo maior se falhar)

## 📈 Monitoramento

Verifique economia frequentemente:
```bash
watch -n 300 "karajan stats"  # A cada 5 minutos
```

---

**Inspiração**: Herbert von Karajan, maestro que orquestrava a berlim Philharmonic com precisão. Assim o Karajan orquestra seus modelos com eficiência. 🎼
