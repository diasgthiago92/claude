# 🎵 Karajan - Cheat Sheet Rápido

## Instalação Rápida

```bash
bash /Users/thiago.dias/Claude_CLI/karajan/setup.sh
source ~/.zshrc
```

## Comandos Principais

| Comando | Uso |
|---------|-----|
| `karajan "tarefa"` | Classificar e obter recomendação de modelo |
| `karajan classify "tarefa"` | Ver nível + modelo em formato legível |
| `karajan stats` | Ver economia de tokens acumulada |
| `karajan history` | Últimas 10 decisões |
| `karajan history 20` | Últimas 20 decisões |

## Exemplos de Uso

### 💰 Cheap (Haiku 4.5) - Economia Máxima
```bash
karajan "Explica esse código"
karajan "Traduz para português"
karajan "Formata esse JSON"
karajan "Corrige typos"
```

### ⚖️ Balanced (Sonnet 5) - Equilíbrio
```bash
karajan "Debug: por que isso não funciona?"
karajan "Refatora esse código"
karajan "Implementa essa feature"
karajan "Escreve testes"
```

### 🚀 Powerful (Opus 5) - Máxima Precisão
```bash
karajan "Redesenha a arquitetura de auth"
karajan "Faz revisão de segurança"
karajan "Otimiza performance"
karajan "Estratégia de migração"
```

## Output Esperado

```json
{
  "level": "cheap",
  "model": "claude-haiku-4-5-20251001",
  "reason": "Tarefa simples - usando Haiku 4.5 para economia máxima",
  "token_weight": 1
}
```

## Estatísticas

```bash
karajan stats
```

Mostra:
- Quantas tarefas em cada nível (Haiku, Sonnet, Opus)
- **Economia % estimada** comparado ao sempre usar Opus
- Total de tarefas roteadas

## Próximas Integrações 🔜

- [ ] Webhook automático: detecção de tarefa → seleção de modelo
- [ ] `/fast` usa Karajan automaticamente
- [ ] Fallback inteligente: falha com Haiku → tenta Sonnet → Opus
- [ ] Dashboard de economia em tempo real

---

**Dica**: Rode `karajan stats` regularmente para monitorar economia!
