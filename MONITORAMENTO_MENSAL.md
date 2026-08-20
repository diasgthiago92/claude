# 📊 Sistema de Monitoramento Mensal de Economia

Acompanhe economia de tokens em tempo real com dashboards automáticos.

---

## 🚀 Como Usar

### Relatório do Mês Atual
```bash
karajan monitor
# ou
karajan report
```

Mostra economia estimada do mês até agora.

### Relatórios Específicos

```bash
# Relatório de hoje
karajan report-today

# Última semana
karajan report-weekly

# Semana anterior
karajan report-weekly 1

# Desde o início do uso
karajan report-all-time
```

---

## 📈 O Que É Monitorado

### Por Tarefa
- ✅ Prompt (primeiros 80 caracteres)
- ✅ Nível selecionado (cheap/balanced/powerful)
- ✅ Modelo usado
- ✅ Tempo de execução
- ✅ Tokens estimados gastos
- ✅ Data/hora

### Agregado (Diário/Semanal/Mensal)
- ✅ Total de tarefas
- ✅ Distribuição por modelo
- ✅ Tokens baseline (se sempre usasse Opus)
- ✅ Tokens reais gastos
- ✅ Economia em tokens
- ✅ Economia em percentual
- ✅ Tempo médio de execução
- ✅ Tarefas por dia

---

## 📊 Exemplo de Relatório Mensal

```
📊 RELATÓRIO MENSAL - 2026-01
======================================================================

📈 Resumo:
  Total de tarefas: 127
  Período: 2026-01-01 a 2026-01-31
  Tarefas por dia: 4.1
  Tempo médio: 1.23s

💰 Economia de Tokens:
  Baseline (sempre Opus): 1,270,000 tokens
  Tokens gastos (com Karajan): 382,000 tokens
  Tokens economizados: 888,000 ✅
  Economia: 69.9% 🎵

  🎵 Karajan economizou 888,000 tokens (69.9%) em 127 tarefas!

📊 Distribuição por Modelo:
  Haiku 4.5: 78 tarefas
  Sonnet 5: 38 tarefas
  Opus 5: 11 tarefas

🔍 Economia por Tipo:
  Tarefas Cheap (Haiku): 702,000 tokens economizados
  Tarefas Balanced (Sonnet): 152,000 tokens economizados
  Tarefas Powerful (Opus): 0 tokens (melhor modelo)

======================================================================
```

---

## 💡 Interpretando os Números

### Baseline vs Actual
- **Baseline**: Se SEMPRE usasse Opus (10x tokens)
- **Actual**: O que realmente gastou (com Karajan)
- **Economia**: Diferença entre os dois

### Exemplo
```
Você usou 127 tarefas

Baseline (127 x Opus):     127 x 10 = 1,270 unidades
Atual (com Karajan):       
  - 78 Haiku (78 x 1)    = 78
  - 38 Sonnet (38 x 5)   = 190
  - 11 Opus (11 x 10)    = 110
  Total                   = 378 unidades

Economia = 1,270 - 378 = 892 unidades = 70.2%
```

---

## 🔄 Integração Automática com Phase 1

Quando você usa `karajan exec`, automaticamente:
1. Executa tarefa
2. Registra nível, tempo, tokens
3. Atualiza monitor.jsonl
4. Próximo relatório já inclui essa tarefa

```bash
karajan exec "sua tarefa"
# ↓
# [Tarefa executada]
# ↓
# [Registrada no monitor]
# ↓
karajan report  # Já mostra essa tarefa!
```

---

## 📁 Arquivos de Dados

### Armazenamento
```
~/.claude_cli/karajan/logs/
├── monitor.jsonl        ← Histórico de cada tarefa (append-only)
├── stats.json          ← Estatísticas agregadas
└── history.jsonl       ← Histórico de decisões Karajan
```

### Formato de monitor.jsonl
```json
{
  "timestamp": "2026-01-15T14:23:45.123456",
  "date": "2026-01-15",
  "prompt_preview": "Explica esse código de autenticação...",
  "level": "balanced",
  "model": "Sonnet 5",
  "execution_time": 1.23,
  "token_weight": 5,
  "tokens_estimated": 342
}
```

---

## 📈 Análises Úteis

### Economia por Tipo de Tarefa
```bash
# Ver qual tipo economiza mais
# Haiku economiza mais? 
# Ou tarefas com Sonnet são melhores custo-benefício?

# Análise manual:
tail -100 ~/.claude_cli/karajan/logs/monitor.jsonl | \
  jq -r '[.level] | group_by(.) | map({level: .[0], count: length})'
```

### Tendência ao Longo do Tempo
```bash
# Ver se economia está melhorando
# Primeiros 10 dias vs últimos 10 dias?

karajan report-weekly 4  # 4 semanas atrás
karajan report-weekly 0  # Última semana
```

### Produtividade
```bash
# Quantas tarefas por dia?
# Tempo médio por tarefa diminuindo?

karajan report  # Vê tarefas por dia
karajan report-today  # Compara com hoje
```

---

## 🎯 Metas de Economia Recomendadas

### Conservador (70% economia)
- ✅ Haiku 60% das tarefas
- ✅ Sonnet 30% das tarefas
- ✅ Opus 10% das tarefas
- **Resultado**: ~70% economia

### Agressivo (80% economia)
- ✅ Haiku 70% das tarefas
- ✅ Sonnet 25% das tarefas
- ✅ Opus 5% das tarefas
- **Resultado**: ~80% economia

### Ultra-Agressivo (90% economia)
- ✅ Haiku 80% das tarefas
- ✅ Sonnet 18% das tarefas
- ✅ Opus 2% das tarefas
- **Resultado**: ~90% economia
- ⚠️ Risco: Respostas ruins em 2% das tarefas

---

## 🔮 Recursos Futuros

### Fase 2: Dashboard Web
```bash
karajan dashboard
# Abre http://localhost:8000/karajan
# Gráficos em tempo real
# Heatmap de economia por hora
```

### Fase 3: Alertas
```bash
# Se economia cair abaixo de 60%
karajan alert-low-economy 60

# Se tokens gastos > esperado
karajan alert-budget 10000
```

### Fase 4: Previsões
```bash
# Quanto você vai economizar até fim do mês?
karajan forecast-month

# Com padrão atual, próximo mês = ?
karajan forecast-next-month
```

---

## 📊 Exemplo: Acompanhamento Semanal

```bash
# Segunda-feira (início da semana)
$ karajan report-weekly
# Mostra economias da última semana

# Sexta-feira (final da semana)
$ karajan report-weekly
# Mostra economias acumuladas (mais completo)

# Segunda seguinte
$ karajan report-weekly
# Mostra semana anterior (para comparação)
```

---

## 🚀 Próximos Passos

1. **Hoje**: Use normalmente com Karajan
2. **Fim de semana**: Rode `karajan report-weekly`
3. **Fim do mês**: Rode `karajan monitor` para relatório mensal
4. **Após 3 meses**: Analise trends em `karajan report-all-time`

---

## 💡 Dicas

### Melhorar Economia
1. Se economia < 70%, aumentar % de tarefas em Haiku
2. Se tarefas em Sonnet falharem, mover para Opus
3. Usar `/fast` para tarefas não-críticas (rota para Haiku)

### Debugging
```bash
# Ver todas as tarefas do mês
tail -500 ~/.claude_cli/karajan/logs/monitor.jsonl | jq .

# Ver modelo mais usado
tail -500 ~/.claude_cli/karajan/logs/monitor.jsonl | \
  jq -r .model | sort | uniq -c

# Ver economia média
tail -500 ~/.claude_cli/karajan/logs/monitor.jsonl | \
  jq '.token_weight' | awk '{sum+=$1} END {print sum/NR}'
```

---

**Comece a monitorar agora:**
```bash
karajan monitor
```

Ao final do mês, você verá exatamente quantos tokens Karajan economizou! 🎵
