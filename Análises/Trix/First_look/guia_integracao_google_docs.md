# Guia de Integração com Google Docs
## Como Automatizar Criação de Documentos no Google

---

## 🔍 O Cenário Atual

**Situação:** Você quer que análises/documentos sejam criados automaticamente no Google Docs

**Problema:** Claude não tem acesso direto à API do Google Docs (por questões de segurança/permissões)

**Solução:** Existem 3 formas de integrar:

---

## ✅ OPÇÃO 1: Apps Script + Google Docs API (Recomendado)

### Como Funciona
1. Você cria um Apps Script no Google Drive
2. O script recebe dados (via webhook ou API)
3. Cria documento no Google Docs automaticamente

### Passo-a-Passo:

#### **Passo 1: Criar o Apps Script**

1. Vá para: https://script.google.com
2. Clique em "Novo Projeto"
3. Copie este código:

```javascript
// Cria documento no Google Docs com conteúdo
function createTrixDocument(conteudo) {
  // Criar documento
  const doc = DocumentApp.create('Trix - Estratégia');
  const body = doc.getBody();
  
  // Adicionar título
  body.appendParagraph('TRIX - Resumo Executivo')
    .setHeading(DocumentApp.ParagraphHeading.TITLE);
  
  // Adicionar data
  body.appendParagraph(new Date().toLocaleDateString('pt-BR'))
    .setForegroundColor('#9ca3af');
  
  // Adicionar conteúdo
  body.appendParagraph(conteudo);
  
  // Compartilhar (opcional)
  doc.addEditor('seu-email@gmail.com');
  
  // Retornar URL do documento
  return doc.getUrl();
}

// Executar manualmente
function onOpen() {
  DocumentApp.getUi()
    .createMenu('Trix')
    .addItem('Criar Documento', 'createTrixDocument')
    .addToUi();
}
```

#### **Passo 2: Configurar Permissões**

1. Clique em "Executar"
2. Google vai pedir permissões
3. Autorize: "Gerenciar documentos"

#### **Passo 3: Testar**

1. Salve o script
2. Volte ao Google Docs
3. Clique em "Trix" → "Criar Documento"
4. ✅ Documento será criado automaticamente

---

## ✅ OPÇÃO 2: Zapier/Make (Sem Código)

### Como Funciona
- Zapier conecta Claude → Google Docs
- Sem necessidade de programar
- Usa webhooks

### Passo-a-Passo:

#### **Passo 1: Criar conta Zapier**
- https://zapier.com (grátis com limite)
- Ou Make.com (melhor para iniciantes)

#### **Passo 2: Criar automação**

**Gatilho (Trigger):**
- Webhook → Recebe dados

**Ação (Action):**
- Google Docs → Criar novo documento

#### **Passo 3: Mapear campos**

```
Input (do Claude):
- Título: "Trix - Estratégia"
- Conteúdo: [texto da análise]
- Email: seu-email@gmail.com

Output (Google Docs):
- Cria documento
- Retorna URL
```

#### **Passo 4: Usar no Claude Code**

Quando você quiser criar documento:
1. Envie dados via curl para webhook Zapier
2. Zapier cria documento no Google Docs
3. Documento fica no seu Drive

**Exemplo de comando:**

```bash
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR-ID/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Trix - Estratégia",
    "content": "Conteúdo aqui...",
    "email": "seu-email@gmail.com"
  }'
```

---

## ✅ OPÇÃO 3: Google Docs Add-on Customizado (Avançado)

### Como Funciona
- Cria um Add-on dentro do Google Docs
- Botão customizado aparece no Docs
- Clica e insere conteúdo

### Vantagem
- Funciona direto no Google Docs
- Sem sair da plataforma

### Exemplo de Code:

```javascript
function onOpen() {
  DocumentApp.getUi()
    .createAddonMenu()
    .addItem('Inserir Análise Trix', 'insertTrixContent')
    .addToUi();
}

function insertTrixContent() {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();
  
  // Títulos
  body.appendParagraph('TRIX')
    .setHeading(DocumentApp.ParagraphHeading.TITLE)
    .setForegroundColor('#22c55e');
  
  body.appendParagraph('Estratégia de Longo Prazo')
    .setHeading(DocumentApp.ParagraphHeading.SUBTITLE);
  
  // Conteúdo
  const content = [
    '1. Resumo Executivo',
    'Trix é uma plataforma de investimento em FII...',
    '',
    '2. Visão 2031',
    'Ser #1 em FII no Brasil...'
  ];
  
  content.forEach(line => {
    body.appendParagraph(line);
  });
  
  DocumentApp.getUi().alert('Análise Trix inserida!');
}
```

---

## 🎯 OPÇÃO 4: Google Sheets → Docs (Integração Simples)

### Como Funciona
1. Dados ficam em Google Sheets
2. Apps Script transforma em Docs
3. Automático a cada atualização

### Exemplo:

```javascript
// Ler dados de planilha e criar documento
function sheetToDoc() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Criar documento
  const doc = DocumentApp.create('Trix - ' + data[0][0]);
  const body = doc.getBody();
  
  // Preencher com dados
  data.forEach((row, index) => {
    body.appendParagraph(row.join(' | '));
  });
  
  Logger.log('Documento criado: ' + doc.getUrl());
}
```

---

## 📊 Comparação das Opções

| Opção | Complexidade | Custo | Tempo Setup | Automação |
|-------|-------------|-------|-----------|-----------|
| **Apps Script** | Média | Grátis | 15 min | ✅ Total |
| **Zapier** | Baixa | $20-30/mês | 5 min | ✅ Total |
| **Add-on** | Alta | Grátis | 30 min | ✅ Manual (clica botão) |
| **Sheets→Docs** | Baixa | Grátis | 10 min | ✅ Automático |

---

## 🚀 RECOMENDAÇÃO PARA VOCÊ

### **Cenário:** Criar análises automaticamente no Google Docs

**Melhor opção: Zapier (Option 2)**

**Por quê:**
- ✅ Sem código
- ✅ Rápido de setup (5 min)
- ✅ Funciona com Claude
- ✅ Documentos direto no Drive
- ✅ Versão free tem limite (100 tasks/mês)

---

## 🔧 SETUP RÁPIDO: Zapier + Google Docs

### Passo 1: Criar Zap

1. Vá para https://zapier.com
2. Clique em "Create" → "New Zap"
3. Escolha trigger: **Webhooks by Zapier** → "Catch Raw Hook"

### Passo 2: Configurar Google Docs

1. Clique em "+ Add action"
2. Busque "Google Docs"
3. Escolha "Create Document"
4. Autorize sua conta Google

### Passo 3: Mapear campos

| Campo Zapier | Valor |
|--|--|
| Document Title | `Trix - {{title}}` |
| Document Body | `{{content}}` |
| Share With Email | `seu-email@gmail.com` |

### Passo 4: Testar

```bash
# Fazer request de teste para Zapier
curl -X POST YOUR-ZAPIER-WEBHOOK-URL \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estratégia Longo Prazo",
    "content": "Este é um teste de integração"
  }'
```

### Passo 5: Usar

Sempre que você quiser criar documento:

```bash
rtk curl -X POST WEBHOOK-URL -d '{"title":"...", "content":"..."}'
```

---

## 💡 ALTERNATIVA AINDA MAIS FÁCIL

**Usar Claude Code com Python + Google API:**

### Setup:

```bash
# Instalar bibliotecas
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Configurar credenciais (one-time)
# Vá para: https://developers.google.com/docs/api/quickstart/python
# Baixe credentials.json e salve no projeto
```

### Script Python:

```python
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_trix_document(title, content):
    auth.authenticate_user()
    docs_service = build('docs', 'v1')
    
    # Criar documento
    doc_body = {
        'title': title
    }
    doc = docs_service.documents().create(body=doc_body).execute()
    doc_id = doc.get('documentId')
    
    # Adicionar conteúdo
    requests = [
        {
            'insertText': {
                'text': content,
                'location': {'index': 1}
            }
        }
    ]
    
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    
    print(f"✅ Documento criado: https://docs.google.com/document/d/{doc_id}")
    return doc_id

# Usar
create_trix_document(
    title="Trix - Estratégia 2031",
    content="Seu conteúdo aqui..."
)
```

---

## 📝 QUAL VOCÊ PREFERE?

1. **Apps Script** → Simples, direto no Google (grátis)
2. **Zapier** → Visual, sem código (pago, mas fácil)
3. **Python + API** → Mais controle, programático
4. **Google Sheets** → Dados → Documento (automático)

---

## ⚙️ PRÓXIMOS PASSOS

Se quiser implementar:

1. **Escolha a opção** (recomendo Zapier ou Apps Script)
2. **Me avise qual**
3. **Vou te guiar no setup passo-a-passo**
4. **Testaremos com a análise Trix**

---

**Qual opção faz mais sentido para você?** 🤔
