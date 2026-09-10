# Repositórios GitHub para CNPJ 🔗

Lista completa de repositórios prontos que você pode usar ou adaptar.

---

## 🌟 TOP 5 Repositórios Recomendados

### 1. BrasilAPI
**Link:** https://github.com/BrasilAPI/brasil-api
**Linguagem:** JavaScript/TypeScript
**Estrelas:** ⭐⭐⭐⭐⭐ (3k+)

**O que é:** API pública com dados de CNPJ, CEP, Telefone, Feriados, etc.

**Vantagens:**
- Sem autenticação necessária
- Documentação excelente
- Rápido e confiável
- Dados atualizados

**Como usar:**
```bash
# Direto pelo curl
curl "https://brasilapi.com.br/api/cnpj/v1/11222333000181"

# Ou com Node.js
npm install brasil-api
```

**Endpoint:**
```
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

**Resposta:**
```json
{
  "cnpj": "11222333000181",
  "razao_social": "FAKE EMPRESA S.A.",
  "logradouro": "RUA FAKE",
  "numero": "123",
  "complemento": "APTO 456",
  "bairro": "CENTRO",
  "municipio": "SAO PAULO",
  "uf": "SP",
  "cep": "01310100",
  "natureza_juridica": "Sociedade Empresária",
  "telefone": "1133334444"
}
```

---

### 2. CNPJrá
**Link:** https://github.com/siderite/cnpjra
**Linguagem:** Python/Shell
**Estrelas:** ⭐⭐⭐⭐ (800+)

**O que é:** CLI completo para consultar CNPJs offline.

**Vantagens:**
- Funciona offline (com dados baixados)
- Rápido
- Fácil de integrar
- Suporta batch processing

**Como usar:**
```bash
pip install cnpjra
cnpjra 11222333000181
cnpjra -f lista.csv
```

---

### 3. Receita Federal - Dados Públicos
**Link:** https://dados.gov.br/dados/datasets/cadastro-nacional-da-pessoa-juridica-cnpj
**Tipo:** Dataset Oficial
**Estrelas:** ⭐⭐⭐⭐⭐ (Fonte oficial)

**O que é:** Dados da Receita Federal em XML/TXT atualizado diariamente.

**Vantagens:**
- Fonte oficial
- Completíssimo
- Dados verificados
- Atualização diária

**Como usar:**
- Download em: https://www.gov.br/pt-br/servicos/consultar-dados-cadastrais-da-empresa
- Ou via FTP da Receita Federal

---

### 4. Serenata de Amor
**Link:** https://github.com/serenata/serenata-de-amor
**Linguagem:** Python
**Estrelas:** ⭐⭐⭐⭐ (1.5k+)

**O que é:** Dados públicos de empresas com análise de integridade.

**Vantagens:**
- Análise de dados públicos
- Flags de empresas suspeitas
- Dados ligados a licitações
- Comunidade ativa

**Como usar:**
```python
from serenata_toolbelt import datasets

companies = datasets.fetch('serenata-companies')
```

---

### 5. CNPJ.me (Validador)
**Link:** https://github.com/carlosflorencio/cnpj.js
**Linguagem:** JavaScript
**Estrelas:** ⭐⭐⭐ (500+)

**O que é:** Validação e formatação de CNPJ.

**Vantagens:**
- Apenas validação (rápido e leve)
- Sem dependências
- Suporta múltiplas linguagens

**Como usar:**
```javascript
const CNPJ = require('cnpj.js');

CNPJ.isValid('11222333000181'); // true
CNPJ.format('11222333000181'); // "11.222.333/0001-81"
```

---

## 🔍 Outros Repositórios Úteis

### Brasil CNPJ (Python)
**Link:** https://github.com/pauloemmilio/brasil-cnpj
- Validação e formatação em Python
- Fácil integração

### CNPJ Validator (Go)
**Link:** https://github.com/fblupi/cnpj-validator
- Validação de CNPJ em Go
- Performance muito boa

### Receita Federal Bot
**Link:** https://github.com/msfidelis/receita-federal-bot
- Bot para consultar CNPJs automaticamente
- Scraping da receita federal

### PyReceita
**Link:** https://github.com/MagoPython/pyreceita
- Biblioteca Python para scraping da Receita Federal
- Mais dados, mais lento

---

## 📊 Matriz de Comparação

| Repo | Validação | Busca | Offline | Dados Completos | Manutenção |
|------|-----------|-------|---------|-----------------|-----------|
| BrasilAPI | ✅ | ✅ | ❌ | ✅ | ✅ Ativo |
| CNPJrá | ✅ | ✅ | ✅ | ⚠️ | ✅ Ativo |
| Receita Federal | ✅ | ✅ | ✅ | ✅✅ | ✅ Oficial |
| Serenata | ⚠️ | ✅ | ✅ | ✅ | ✅ Ativo |
| CNPJ.js | ✅ | ❌ | ✅ | ❌ | ✅ Ativo |

---

## 🛠️ Como Contribuir/Adaptar

Se quiser usar um desses repositórios:

```bash
# Clonar
git clone <url-do-repo>

# Instalar dependências
cd <repo>
pip install -r requirements.txt  # ou npm install

# Usar/Testar
python main.py  # ou npm start
```

---

## ⚠️ Notas Importantes

1. **BrasilAPI** tem rate limit (use com moderação)
2. **Receita Federal** tem dados XML grandes (podem ser lentos)
3. **Serenata** tem foco em análise, não só busca
4. **CNPJrá** precisa de download inicial de dados

---

**Última atualização:** 2026-09-09
