# 📚 Sistema de Índice - Claude CLI

## O que é?

Um sistema automático que mapeia **tudo** que você tem configurado no Claude CLI:
- ⚙️ Settings & Configurações
- 🔗 MCP Servers (Google Docs, Slides, Drive, Gmail)
- 🎯 Skills
- 📁 Projetos & Análises
- 💾 Memória Persistente
- ⏰ Rotinas & Agendamentos

---

## 📂 Arquivos Criados

### 1. **INDEX.md** ⭐
O arquivo principal que lista tudo:
- Localização: `/Users/thiago.dias/Claude_CLI/INDEX.md`
- Atualizado: automaticamente a cada geração
- Conteúdo: Mapa completo de todo o Claude CLI

**Abrir:**
```bash
cat /Users/thiago.dias/Claude_CLI/INDEX.md
```

---

### 2. **generate-index.py**
Script Python que gera o índice:
- Localização: `/Users/thiago.dias/Claude_CLI/scripts/generate-index.py`
- Função: Escaneia e mapeia tudo
- Execução: Manual ou via rotina

**Rodar:**
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

---

### 3. **index-manager.sh** 🎯
Gerenciador de linha de comando:
- Localização: `/Users/thiago.dias/Claude_CLI/scripts/index-manager.sh`
- Funções: Visualizar, buscar, monitorar
- Interface: Amigável com cores

**Comandos:**
```bash
./scripts/index-manager.sh generate   # Gerar/atualizar
./scripts/index-manager.sh show       # Ver completo
./scripts/index-manager.sh mcp        # Ver apenas MCP
./scripts/index-manager.sh search "termo"  # Buscar
./scripts/index-manager.sh watch      # Monitorar
./scripts/index-manager.sh stats      # Ver stats
```

---

### 4. **CONFIG_ROTINAS.md**
Documentação de configurações automáticas:
- Localização: `/Users/thiago.dias/Claude_CLI/CONFIG_ROTINAS.md`
- Conteúdo: Como configurar rotinas
- Exemplos: Agendamento automático

---

## 🚀 Como Usar

### **Opção 1: Visualizar Index Completo**
```bash
cat /Users/thiago.dias/Claude_CLI/INDEX.md
```

Ou com `less` (para paginação):
```bash
less /Users/thiago.dias/Claude_CLI/INDEX.md
```

---

### **Opção 2: Usar Index Manager**

#### Ver tudo
```bash
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh show
```

#### Ver apenas MCP Servers
```bash
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh mcp
```

#### Buscar por termo
```bash
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh search "google"
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh search "trix"
```

#### Monitorar em tempo real
```bash
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh watch
```

---

### **Opção 3: Criar Alias (Recomendado)**

Adicione ao seu `.zshrc` ou `.bashrc`:

```bash
# Alias para o Index Manager
alias index="bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh"
alias index-gen="python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py"
```

Depois use:
```bash
index show
index search "trix"
index mcp
index-gen
```

---

## 📊 O que o Índice Mapeia

### ⚙️ Settings
- Global settings (`~/.claude/settings.json`)
- Local settings (`~/.claude/settings.local.json`)
- Configurações ativas

### 🔗 MCP Servers
- google-docs ✅
- google-slides ✅
- google-drive ✅
- gmail ✅

### 📁 Projetos
- Trix (análises)
- Outros projetos

### 💾 Memória
- workspace_organization_rules
- user_main_workspace
- project_karajan
- feedback_language_portuguese
- backup_procedure

### 🎯 Scripts
- generate-index.py
- create_google_doc.py
- index-manager.sh
- Outros scripts

---

## 🔄 Atualizar Índice

### **Manual**
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

### **Automático (Rotina)**

Configurar via `/schedule`:
```
/schedule create
  Name: Update Claude CLI Index
  Schedule: Every Sunday at 9:00 AM
  Command: python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

Ou via comando:
```bash
claude schedule create \
  --name "update-claude-index" \
  --schedule "0 9 * * 0" \
  --command "python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py"
```

---

## 🎯 Casos de Uso

### **1. Encontrar um MCP Server**
```bash
index search "google-docs"
```

### **2. Ver todos os scripts Python**
```bash
index search "\.py"
```

### **3. Ver configuração atual**
```bash
index settings
```

### **4. Monitorar mudanças**
```bash
index watch
# Atualiza a cada 10 segundos
```

### **5. Contar projetos**
```bash
index projects
```

---

## 📈 Resumo Rápido (Atual)

```
✅ MCP Servers:      4 ativo(s)
✅ Scripts:          2+ arquivo(s)
✅ Projetos:         1+ projeto(s)
✅ Memória:          6+ arquivo(s)
✅ Skills:           0+ skill(s)
```

---

## 🔐 Segurança

✅ Lê apenas arquivos públicos  
✅ Não modifica nada  
✅ Arquivo gerado localmente  
✅ Sem envio de dados para cloud  

---

## 🚨 Troubleshooting

### "Comando não encontrado"
```bash
# Use o caminho completo
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh [comando]

# Ou crie um alias no .zshrc
alias index="bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh"
```

### "Índice está desatualizado"
```bash
python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

### "Não encontra MCP servers"
```bash
# Verifique settings.json
cat ~/.claude/settings.json | grep mcpServers

# Regenere o índice
python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
```

---

## 💡 Dicas

1. **Use Cmd+F no INDEX.md** para buscar rapidamente
2. **Crie um alias** para usar `index` de qualquer lugar
3. **Monitore com `watch`** para ver mudanças em tempo real
4. **Atualize regularmente** (configurado em rotina)

---

## 🎉 Pronto!

```bash
# Teste agora:
bash /Users/thiago.dias/Claude_CLI/scripts/index-manager.sh stats

# Ou veja o index completo:
cat /Users/thiago.dias/Claude_CLI/INDEX.md
```

---

**Sistema de índice ativado e funcionando!** 📚✨
