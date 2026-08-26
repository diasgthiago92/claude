# Setup MCP - Google Docs Integration

## ✅ Objetivo
Configurar MCP para que Claude Code acesse Google Docs diretamente.

---

## 📋 Passo-a-Passo

### Passo 1: Instalar dependências

```bash
cd /Users/thiago.dias/Claude_CLI/mcp

npm install googleapis @anthropic-ai/sdk
```

### Passo 2: Verificar se arquivo de credenciais existe

Credenciais esperadas em:
```
~/Downloads/thiagodias-30c5309274a4.json
```

✅ Você já tem este arquivo? (do Google Console)

### Passo 3: Testar o servidor MCP

```bash
cd /Users/thiago.dias/Claude_CLI/mcp

node google-docs-server.js
```

Deve mostrar:
```
🚀 Iniciando MCP Server para Google Docs...
✅ Autenticação com Google OK
✅ MCP Server pronto!
```

### Passo 4: Configurar Claude Code

Abra o arquivo de configuração:
```
~/.claude/settings.json
```

Ou use o comando:
```bash
claude config
```

### Passo 5: Adicionar servidor MCP

Adicione isto ao settings.json:

```json
{
  "mcpServers": {
    "google-docs": {
      "command": "node",
      "args": ["/Users/thiago.dias/Claude_CLI/mcp/google-docs-server.js"],
      "env": {
        "HOME": "/Users/thiago.dias",
        "NODE_PATH": "/usr/local/lib/node_modules"
      },
      "disabled": false
    }
  }
}
```

### Passo 6: Restart Claude Code

1. Feche Claude Code (se estiver aberto)
2. Abra novamente

### Passo 7: Verificar MCP

No terminal do Claude Code, rode:
```bash
claude info
```

Deve listar o MCP server "google-docs"

---

## 🎯 Ferramentas Disponíveis (via MCP)

Depois de configurado, terei acesso a:

### 1. Criar Documento
```
create_google_doc(title, content)
```
Exemplo: Criar "Trix - Estratégia" com conteúdo

### 2. Ler Documento
```
read_google_doc(documentId)
```
Exemplo: Ler conteúdo de um documento existente

### 3. Listar Documentos
```
list_google_docs(limit)
```
Exemplo: Listar últimos 10 documentos

### 4. Compartilhar Documento
```
share_google_doc(documentId, email, role)
```
Exemplo: Compartilhar com seu-email@gmail.com

---

## 🚀 Uso (Depois de Configurado)

Você poderá me pedir:

```
"Crie um documento no Google Docs chamado 'Trix - Análise' 
com o conteúdo de estrategia_cpo_longo_prazo.md"
```

E eu vou:
1. ✅ Ler o arquivo
2. ✅ Criar documento no seu Google
3. ✅ Adicionar o conteúdo
4. ✅ Retornar o link

---

## ⚠️ Troubleshooting

### Erro: "Credenciais não encontradas"
```
Solução: Verifique se thiagodias-30c5309274a4.json está em ~/Downloads/
```

### Erro: "MCP server not found"
```
Solução: 
1. Verifique settings.json está correto
2. Restart Claude Code
3. Rode: claude info
```

### Erro: "googleapis not installed"
```
Solução: 
cd /Users/thiago.dias/Claude_CLI/mcp
npm install googleapis
```

---

## ✅ Próximos Passos

1. [ ] Instale dependências (npm install)
2. [ ] Teste servidor (node google-docs-server.js)
3. [ ] Adicione MCP ao settings.json
4. [ ] Restart Claude Code
5. [ ] Me avisa que está pronto!

---

**Quando tiver pronto, me avisa que posso começar a criar docs no Google!** 🚀
