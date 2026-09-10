# CNPJ Explorer 🇧🇷

Solução completa para consultar informações de CNPJs brasileiros com múltiplas opções e integrações.

## 📋 Conteúdo

1. **Repositórios Existentes** — Soluções prontas no GitHub
2. **CLI Próprio** — Ferramenta customizada para sua necessidade
3. **APIs e Integrações** — Formas de conectar dados
4. **Exemplos Práticos** — Casos de uso reais

---

## 1️⃣ Repositórios GitHub Existentes

Ver: [REPOSITORIOS_GITHUB.md](./docs/REPOSITORIOS_GITHUB.md)

**Destaques:**
- **BrasilAPI** — API pública com dados de CNPJ, CEP e mais
- **CNPJrá** — Ferramenta CLI pronta para usar
- **Dados Públicos Receita Federal** — Fonte oficial de dados
- **Validador CNPJ** — Apenas para validação de formato

---

## 2️⃣ CLI Próprio

Ver: [CLI.md](./docs/CLI.md)

**Usar:**
```bash
cd /Users/thiago.dias/Claude_CLI/cnpj-explorer
python cli/cnpj_cli.py --cnpj 11222333000181
python cli/cnpj_cli.py --search "Amazon"
python cli/cnpj_cli.py --csv lista_cnpjs.csv
```

**Recursos:**
- Busca por CNPJ ou razão social
- Validação de formato
- Exportação em JSON/CSV
- Cache local
- Modo batch

---

## 3️⃣ APIs de Integração

Ver: [INTEGRACAO_APIS.md](./docs/INTEGRACAO_APIS.md)

**Opções:**
1. **BrasilAPI** (gratuita, sem autenticação)
2. **Receita Federal** (dados oficiais, setup mais complexo)
3. **Serenata de Amor** (dados públicos + análise)
4. **Meu CNPJ** (API paga, dados atualizados em tempo real)

---

## 4️⃣ Exemplos Práticos

Ver: [examples/](./examples/)

- `validate_cnpj.py` — Validação básica
- `search_and_export.py` — Busca com exportação
- `batch_processing.py` — Processar múltiplos CNPJs
- `brasilapi_integration.py` — Integrar com BrasilAPI
- `receita_federal_integration.py` — Integrar com Receita Federal

---

## 🚀 Quick Start

### Opção 1: Usar BrasilAPI (mais simples)
```bash
curl "https://brasilapi.com.br/api/cnpj/v1/11222333000181"
```

### Opção 2: Usar CLI próprio
```bash
python cli/cnpj_cli.py --cnpj 11222333000181
```

### Opção 3: Integrar em seu código
```python
from apis.brasilapi import buscar_cnpj

dados = buscar_cnpj("11222333000181")
print(dados)
```

---

## 📊 Comparação de Soluções

| Solução | Facilidade | Dados | Atualização | Custo |
|---------|-----------|-------|-------------|-------|
| BrasilAPI | ⭐⭐⭐⭐⭐ | Básicos | Semanal | Gratuita |
| CLI Próprio | ⭐⭐⭐⭐ | Personalizável | Configurável | Grátis |
| Receita Federal | ⭐⭐⭐ | Completos | Diário | Gratuita |
| Meu CNPJ (API) | ⭐⭐⭐⭐ | Completos | Tempo real | Paga |

---

## 🔧 Instalação

```bash
cd /Users/thiago.dias/Claude_CLI/cnpj-explorer
chmod +x install.sh
./install.sh
```

---

## 📞 Próximos Passos

1. Escolha qual solução usar: [COMPARACAO.md](./docs/COMPARACAO.md)
2. Leia o guia específico: [cli/](./cli/) ou [docs/INTEGRACAO_APIS.md](./docs/INTEGRACAO_APIS.md)
3. Teste com exemplos: [examples/](./examples/)
4. Customize conforme necessário

---

**Última atualização:** 2026-09-09
**Criador:** Claude Code
