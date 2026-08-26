# ⏰ Rotinas & Agendamentos - Claude CLI

## 📋 Resumo

Configurações de rotinas automáticas para manter o Claude CLI organizado e atualizado.

---

## 🔄 Rotina: Atualizar Índice

### Descrição
Atualiza automaticamente o índice de configurações, skills, MCP servers, etc.

### Frequência
- **Inicial:** A cada 7 dias
- **Manual:** `python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py`

### Como Configurar (CronCreate)

```bash
claude schedule create \
  --name "update-claude-index" \
  --schedule "0 9 * * 0" \
  --command "python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py"
```

Ou via `/schedule`:
```
/schedule create
  Name: Update Claude CLI Index
  Schedule: Every Sunday at 9:00 AM
  Command: python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

### Verificar Rotinas
```bash
claude schedule list
```

---

## 🛠️ Ferramentas Rápidas

### Gerar Índice
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

### Usar Index Manager
```bash
chmod +x /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh

# Gerar índice
./scripts/index-manager.sh generate

# Ver índice
./scripts/index-manager.sh show

# Buscar
./scripts/index-manager.sh search "trix"

# Monitorar
./scripts/index-manager.sh watch

# Ver stats
./scripts/index-manager.sh stats
```

---

## 📊 Arquivos Gerados

### `INDEX.md`
- ✅ Índice completo do Claude CLI
- ✅ Mapeia: settings, MCP, skills, projetos, memória
- ✅ Atualizado automaticamente
- ✅ Locação: `/Users/thiago.dias/Claude_CLI/INDEX.md`

### `generate-index.py`
- Script Python que gera o índice
- Escaneia estrutura do Claude_CLI
- Lê configurações
- Mapeia MCP servers

### `index-manager.sh`
- Gerenciador de índice
- Comandos: generate, show, search, watch, stats
- Interface amigável

---

## 🎯 Estrutura Monitorada

```
🔍 Escaneia:
  ├── Settings (.claude/settings.json)
  ├── Local Settings (.claude/settings.local.json)
  ├── MCP Servers
  ├── Skills
  ├── Scripts (Python/Shell)
  ├── Projetos/Análises
  └── Memória Persistente
```

---

## 💡 Casos de Uso

### 1. Encontrar um Script
```bash
./scripts/index-manager.sh search "google"
```

### 2. Ver Todos os MCP Servers
```bash
./scripts/index-manager.sh mcp
```

### 3. Monitorar Mudanças em Tempo Real
```bash
./scripts/index-manager.sh watch
```

### 4. Ver Estatísticas
```bash
./scripts/index-manager.sh stats
```

### 5. Buscar por Projeto
```bash
./scripts/index-manager.sh search "trix"
```

---

## 🔐 Rotina de Backup (Futura)

```bash
# Opcional: Backup do INDEX
/schedule create
  Name: Backup Claude Index
  Schedule: Every day at 11:59 PM
  Command: cp /Users/thiago.dias/Claude_CLI/INDEX.md /Users/thiago.dias/Claude_CLI/backups/INDEX-$(date +%Y%m%d).md
```

---

## 📝 Como Adicionar Novas Rotinas

1. **Criar script** em `/Users/thiago.dias/Claude_CLI/scripts/`
2. **Testar manualmente** antes
3. **Adicionar à rotina** com `/schedule create`
4. **Rerun** `generate-index.py` para atualizar

Exemplo:
```bash
# Seu script
vim /Users/thiago.dias/Claude_CLI/scripts/daily-cleanup.sh

# Testar
bash /Users/thiago.dias/Claude_CLI/scripts/daily-cleanup.sh

# Agendar
/schedule create
  Name: Daily Cleanup
  Schedule: Every day at 2:00 AM
  Command: bash /Users/thiago.dias/Claude_CLI/scripts/daily-cleanup.sh
```

---

## ✅ Checklist de Configuração

- [ ] `generate-index.py` existe e funciona
- [ ] `index-manager.sh` tem permissão de execução
- [ ] `INDEX.md` foi gerado
- [ ] Rotina de atualização agendada (opcional)
- [ ] Testou os comandos do index-manager

---

## 🚀 Próximas Etapas

1. **Executar:**
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
   ```

2. **Visualizar:**
   ```bash
   cat /Users/thiago.dias/Claude_CLI/INDEX.md
   ```

3. **Testar Index Manager:**
   ```bash
   bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh help
   ```

4. **Agendar rotina** (opcional):
   ```bash
   /schedule create ... (veja acima)
   ```

---

**Tudo pronto para manter o Claude CLI organizado!** 🎉
