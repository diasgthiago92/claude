# Script: Criar Documentos no Google Docs Automaticamente

**Arquivo:** `create_google_doc.py`

---

## 🔒 Segurança

Este script:
- ✅ Roda **localmente** no seu computador
- ✅ Usa **credenciais locais** (arquivo JSON)
- ✅ Nunca compartilha suas chaves
- ✅ Comunica diretamente com Google Docs API

---

## 📦 Instalação (primeira vez)

### Passo 1: Instalar bibliotecas
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

### Passo 2: Credenciais já estão em
```
~/Downloads/thiagodias-30c5309274a4.json
```

✅ Pronto! Não precisa fazer nada mais.

---

## 🚀 Como Usar

### Opção 1: Criar documento simples
```bash
python create_google_doc.py "Meu Documento"
```

### Opção 2: Com conteúdo
```bash
python create_google_doc.py "Trix - Estratégia" "Conteúdo aqui"
```

### Opção 3: Com conteúdo + compartilhar
```bash
python create_google_doc.py "Trix" "Análise completa" "seu-email@gmail.com"
```

---

## 📝 Exemplos Práticos

### Criar documento com análise Trix:
```bash
python create_google_doc.py \
  "Trix - Resumo Executivo" \
  "Visão: Ser #1 em FII no Brasil\n\nMercado: R$ 500B AUM\nUsuários: Apenas 2M investem em FII"
```

### Ler de arquivo e criar:
```bash
CONTENT=$(cat /Users/thiago.dias/Claude_CLI/Análises/Trix/First_look/resumo_executivo.html)

python create_google_doc.py "Trix - Análise HTML" "$CONTENT"
```

### Criar a partir de Markdown:
```bash
CONTENT=$(cat /Users/thiago.dias/Claude_CLI/Análises/Trix/First_look/estrategia_cpo_longo_prazo.md)

python create_google_doc.py "Trix - Estratégia" "$CONTENT"
```

---

## ✅ O que o script faz

1. ✅ Autentica com suas credenciais Google
2. ✅ Cria novo documento no Google Docs
3. ✅ Adiciona conteúdo (texto, markdown, HTML)
4. ✅ Compartilha com email (opcional)
5. ✅ Retorna URL para acessar

---

## 📊 Output Esperado

```
📝 Criando documento: 'Trix - Estratégia'...
✅ Documento criado: https://docs.google.com/document/d/1xyzABC...
📄 Adicionando conteúdo (5000 caracteres)...
✅ Conteúdo adicionado
🔗 Compartilhando com seu-email@gmail.com...
✅ Compartilhado

🎉 Sucesso! Acesse: https://docs.google.com/document/d/1xyzABC...
```

---

## 🛠️ Troubleshooting

### Erro: "Arquivo de credenciais não encontrado"
```
Solução: Verifique se thiagodias-30c5309274a4.json está em ~/Downloads/
```

### Erro: "Permission denied"
```
Solução: Credenciais vencidas. Crie novas em:
https://console.cloud.google.com/apis/credentials
```

### Erro: "API not enabled"
```
Solução: Ative a Google Docs API:
1. Vá para https://console.cloud.google.com/apis/library
2. Busque "Google Docs API"
3. Clique em "Enable"
```

---

## 🔄 Automatizar com Claude Code

### Criar análise + documento automaticamente:

```bash
#!/bin/bash

# Gerar análise (seu comando aqui)
ANALYSIS="Trix é uma plataforma de FII..."

# Criar documento
python /Users/thiago.dias/Claude_CLI/scripts/create_google_doc.py \
  "Trix - Análise Automática" \
  "$ANALYSIS" \
  "seu-email@gmail.com"

echo "✅ Documento criado com sucesso!"
```

---

## 💡 Ideias de Uso

1. **Análises automáticas** → Google Docs
2. **Relatórios** → Documento compartilhado
3. **Apresentações** → Exportar para PowerPoint
4. **Arquivamento** → Tudo no Drive

---

## 📞 Suporte

Se tiver problemas:
1. Verifique se a API está ativada
2. Confirme credenciais estão corretas
3. Teste com documento simples primeiro

---

**Script pronto para usar!** 🚀
