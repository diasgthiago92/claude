# 📚 Índice Completo - Claude CLI

**Atualizado em:** 26/08/2026 14:48:15

---

## ⚙️ Settings & Configurações

### Global Settings (`~/.claude/settings.json`)

```json

{
  "model": "haiku",
  "theme": "dark-ansi",
  "agentPushNotifEnabled": true,
  "karajan": {
    "enabled": true,
    "version": "phase-1-with-rtk",
    "description": "Roteamento automático de modelos + economia RTK"
  },
  "rtk": {
    "enabled": true,
    "description": "RTK comprime automaticamente (60-90% economia)"
  },
  "mcpServers": {
    "google-docs": {
      "command": "node",
      "args": [
        "/Users/thiago.dias/Claude_CLI/mcp/google-docs-server.js"
      ],
      "disabled"

...
```

### Local Settings (`~/.claude/settings.local.json`)

Configurações locais ativadas ✅



## 🔗 MCP Servers (Integrações)

### google-docs ✅ Ativo

- **Command:** `node`

- **Args:** /Users/thiago.dias/Claude_CLI/mcp/google-docs-server.js...



### google-slides ✅ Ativo

- **Command:** `node`

- **Args:** /Users/thiago.dias/Claude_CLI/mcp/google-slides-server.js...



### google-drive ✅ Ativo

- **Command:** `node`

- **Args:** /Users/thiago.dias/Claude_CLI/mcp/google-drive-server.js...



### gmail ✅ Ativo

- **Command:** `node`

- **Args:** /Users/thiago.dias/Claude_CLI/mcp/google-gmail-server.js...



## 🎯 Skills Disponíveis

Nenhuma skill encontrada



## 📁 Estrutura Claude_CLI

### Scripts Python/Shell

- `create_google_doc.py`

- `generate-index.py`



### MCP Servers

- `google-slides-server.js`

- `google-docs-server.js`

- `google-gmail-server.js`

- `google-drive-server.js`



### Projetos/Análises

- **Trix**



### Memória Persistente

- workspace_organization_rules

- user_main_workspace

- project_karajan

- MEMORY

- feedback_language_portuguese

- backup_procedure



## ⏰ Rotinas & Agendamentos

### Verificar com:

```bash
claude schedule list
```



## 🚀 Como Usar Este Índice


1. **Atualizar Index:**
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
   ```

2. **Ver Index:**
   ```bash
   cat /Users/thiago.dias/Claude_CLI/INDEX.md
   ```

3. **Auto-atualizar (rotina):**
   - Configurado em CronCreate cada 7 dias

4. **Buscar algo:**
   - Use Cmd+F no arquivo INDEX.md
   - Procure por nome do skill, MCP, script, etc


## 📊 Resumo Rápido

- **MCP Servers:** 4 ativo(s)

- **Scripts:** 2 arquivo(s)

- **Projetos:** 1 projeto(s)

- **Memória:** 6 arquivo(s)

- **Skills:** 0 skill(s)
