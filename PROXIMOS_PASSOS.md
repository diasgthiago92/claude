# 🎵 Karajan: Próximos Passos para Tornar Default

Atualmente o Karajan funciona como CLI manual. Para torná-lo o **modelo default** automático, há várias estratégias:

## Opção 1: Hook no Claude Code (Recomendado)

Criar um hook que intercepta toda requisição e seleciona modelo automaticamente.

```bash
# Seria adicionado ao settings.json do Claude Code:
{
  "hooks": {
    "before:submit": "karajan classify | extract-model-and-set"
  }
}
```

**Vantagem**: Automático, transparente
**Desafio**: Requer integração com Claude Code API

## Opção 2: Wrapper Shell

Criar um wrapper que substitui `claude` ou `c`:

```bash
# ~/.local/bin/c (wrapper)
#!/bin/bash
prompt="$@"
model=$(karajan "$prompt" | jq -r .model)
claude --model "$model" "$prompt"
```

**Vantagem**: Funciona hoje, simples
**Desafio**: Precisa ser usado em lugar de `claude` direto

## Opção 3: Fallback Inteligente

Quando qualquer tarefa falhar (tokens, timeout, erro):
1. Começa com modelo predicted pelo Karajan
2. Se falhar → tenta com modelo 1 nível acima
3. Se ainda falhar → full Opus

```python
# No orchestrator.py
def execute_with_fallback(prompt, preferred_level):
    for level in [preferred_level, "balanced", "powerful"]:
        try:
            result = call_claude(level, prompt)
            return result
        except Exception:
            continue
    raise Exception("All models failed")
```

## Opção 4: Integração com /fast

O `/fast` é Sonnet mais rápido. Poderia ser:

```
/fast → Karajan roteamento automático
  ✅ Haiku se simples
  ✅ Sonnet se médio (mesmo que /fast intuitivamente)
  ✅ Opus se complexo
```

## Estratégia Recomendada (MVP → Produção)

### MVP Atual ✅
- CLI manual: `karajan "tarefa"`
- Logging de decisões
- Estatísticas de economia

### Fase 1: Alias Atalho (Semana 1)
```bash
alias c="karajan_wrapper"  # Faz análise + chama Claude com modelo certo
```

### Fase 2: Hook de Classificação Automática (Semana 2)
- Integrar com Claude Code hook system
- Detecta tipo de tarefa automaticamente
- Seleciona modelo antes de submeter

### Fase 3: Fallback Inteligente (Semana 3)
- Se falhar com Haiku → tenta Sonnet
- Se falhar com Sonnet → tenta Opus
- Registra qual foi o nível necessário (feedback loop)

### Fase 4: Dashboard em Tempo Real (Semana 4)
- WebUI mostrando economia
- Histórico detalhado por tipo de tarefa
- Recomendações de otimização

## Como Fazer Hoje

Para começar a usar Karajan como seu modelo "default":

```bash
# 1. Instalar alias
bash /Users/thiago.dias/Claude_CLI/karajan/setup.sh

# 2. Sempre usar assim:
karajan "minha tarefa"

# 3. Verificar economia:
karajan stats
```

## Arquivo de Configuração para Integração Futura

Quando/se integrar com Claude Code, adicionar ao `~/.claude/settings.json`:

```json
{
  "karajan": {
    "enabled": true,
    "auto_select_model": true,
    "fallback_on_error": true,
    "log_decisions": true,
    "aggressive_savings": false
  }
}
```

---

**Objetivo Final**: Você não precisa pensar em qual modelo usar — Karajan escolhe automaticamente o melhor custo-benefício para cada tarefa.

Quer começar com qual fase? 🎼
