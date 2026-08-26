# 📊 Token Usage Tracker

Sistema de rastreamento diário de uso de tokens do Claude CLI.

---

## O que é?

Um sistema automático que:
- ✅ Registra uso de tokens diariamente
- ✅ Gera relatórios (diário, semanal, mensal)
- ✅ Mostra economia RTK (60-90%)
- ✅ Exporta para CSV
- ✅ Dashboard visual

---

## 🚀 Como Usar

### **Opção 1: Rastrear Uso Manual**

```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py log \
  --tokens 4000 \
  --category coding \
  --description "Script implementation"
```

### **Opção 2: Ver Relatórios**

#### Relatório diário
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py daily
```

#### Relatório semanal
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py weekly
```

#### Relatório mensal
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py monthly
```

#### Estimativa
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py estimate
```

### **Opção 3: Exportar para CSV**

```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py export
```

### **Opção 4: Relatório Automático Diário**

```bash
bash /Users/thiago.dias/Claude_CLI/scripts/daily-token-report.sh
```

### **Opção 5: Ver Dashboard**

```bash
open /Users/thiago.dias/Claude_CLI/scripts/token-dashboard.html
```

---

## 📁 Arquivos

### **token-tracker.py** ⭐
Script principal com todas as funções:
- log: Registrar tokens
- daily: Relatório diário
- weekly: Relatório semanal
- monthly: Relatório mensal
- estimate: Estimativa
- export: Exportar CSV

### **daily-token-report.sh**
Script que gera o relatório completo:
- Relatório diário
- Relatório semanal
- Estimativa
- Exportação CSV

### **token-dashboard.html**
Dashboard visual com gráficos:
- Uso semanal (gráfico de linha)
- Distribuição por categoria (pie chart)
- Tabela de dados
- Estatísticas em tempo real

---

## 🔄 Configurar Rotina Automática

### Via `/schedule`:

```bash
/schedule create
  Name: Daily Token Report
  Schedule: Every day at 11:59 PM
  Command: bash /Users/thiago.dias/Claude_CLI/scripts/daily-token-report.sh
```

### Verificar:
```bash
claude schedule list
```

---

## 📊 Estrutura de Dados

### Arquivo JSON diário
```
/Users/thiago.dias/Claude_CLI/logs/token-usage/tokens-2026-08-26.json

{
  "date": "2026-08-26",
  "entries": [
    {
      "timestamp": "2026-08-26T14:30:00",
      "tokens": 4000,
      "category": "analysis",
      "description": "Generated Trix index"
    }
  ],
  "summary": {
    "total_tokens": 4000,
    "num_interactions": 1,
    "avg_tokens": 4000,
    "last_update": "2026-08-26T14:30:00"
  }
}
```

### CSV Export
```
Date,Time,Tokens,Category,Description
2026-08-26,14:30:00,4000,analysis,Generated Trix index
```

---

## 🎯 Categorias Disponíveis

- **general** - Interações gerais
- **analysis** - Análise de dados/código
- **coding** - Implementação de código
- **mcp** - Uso de MCP servers
- **research** - Pesquisa/investigação

---

## 💡 Exemplos

### Logar análise do Trix
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py log \
  --tokens 8500 \
  --category analysis \
  --description "Trix strategy analysis and documentation"
```

### Logar implementação de MCP
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py log \
  --tokens 6000 \
  --category mcp \
  --description "Google Docs MCP server setup"
```

### Ver relatório semanal
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py weekly
```

### Exportar e abrir no Numbers
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py export
open /Users/thiago.dias/Claude_CLI/logs/token-usage/tokens-export-*.csv
```

---

## 📈 Estatísticas Rastreadas

- **Total de tokens** (diário, semanal, mensal)
- **Número de interações**
- **Média de tokens por interação**
- **Distribuição por categoria**
- **Economia RTK** (60-90% de redução)
- **Tendências** (crescimento/queda)

---

## 🔐 Dados Privados

✅ Todos os dados são armazenados localmente  
✅ Sem envio para cloud  
✅ Acesso apenas de você  

Localização: `/Users/thiago.dias/Claude_CLI/logs/token-usage/`

---

## 📊 Dashboard em Tempo Real

Para visualizar dados atualizados:

1. Abra o dashboard:
   ```bash
   open /Users/thiago.dias/Claude_CLI/scripts/token-dashboard.html
   ```

2. Gere dados com:
   ```bash
   bash /Users/thiago.dias/Claude_CLI/scripts/daily-token-report.sh
   ```

3. Recarregue o dashboard (Cmd+R)

---

## ⏰ Automação Recomendada

### Setup inicial:
```bash
# Criar rotina diária
/schedule create
  Name: Daily Token Report
  Schedule: Every day at 11:59 PM
  Command: bash /Users/thiago.dias/Claude_CLI/scripts/daily-token-report.sh

# Verificar
claude schedule list
```

Depois disso, o relatório será gerado automaticamente todo dia!

---

## 🚀 Próximos Passos

1. ✅ Teste o tracker:
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py estimate
   ```

2. ✅ Log sua primeira interação:
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py log \
     --tokens 5000 --category general --description "Test"
   ```

3. ✅ Ver relatório:
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/token-tracker.py daily
   ```

4. ✅ (Opcional) Configure rotina automática

5. ✅ Visualize no dashboard

---

## 📞 Troubleshooting

### "FileNotFoundError"
```
→ Verifique se /Users/thiago.dias/Claude_CLI/logs/token-usage/ existe
→ Crie: mkdir -p /Users/thiago.dias/Claude_CLI/logs/token-usage/
```

### "ModuleNotFoundError"
```
→ Instale dependências: pip3 install [módulo]
```

### Dashboard não carrega dados
```
→ Certifique-se de ter registrado tokens
→ Recarregue a página (Cmd+R)
```

---

## 📝 Próximos Recursos (Futuros)

- [ ] Integração com Google Sheets
- [ ] Alertas (quando tokens excedem limite)
- [ ] Comparação mensal automática
- [ ] Gráficos interativos avançados
- [ ] Exportação PDF
- [ ] Análise de tendências com ML

---

**Token tracking ativado!** 📊✨
