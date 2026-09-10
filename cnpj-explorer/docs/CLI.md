# CLI Próprio - CNPJ Explorer 🖥️

Ferramenta customizada para sua necessidade específica de consultar CNPJs.

---

## Instalação

```bash
cd /Users/thiago.dias/Claude_CLI/cnpj-explorer
pip install -r requirements.txt
chmod +x cli/cnpj_cli.py
```

---

## Uso Básico

### 1. Validar CNPJ

```bash
python cli/cnpj_cli.py --validate 11222333000181
```

**Resposta:**
```
✅ CNPJ válido
Formatado: 11.222.333/0001-81
```

---

### 2. Buscar por CNPJ

```bash
python cli/cnpj_cli.py --cnpj 11222333000181
```

**Resposta:**
```json
{
  "cnpj": "11222333000181",
  "razao_social": "FAKE EMPRESA S.A.",
  "endereco": "RUA FAKE, 123 - CENTRO - SAO PAULO - SP",
  "cep": "01310100",
  "telefone": "1133334444",
  "natureza_juridica": "Sociedade Empresária"
}
```

---

### 3. Buscar por Nome/Razão Social

```bash
python cli/cnpj_cli.py --search "Amazon"
```

**Resposta:**
```
Encontrados 5 resultados:

1. AMAZON BRASIL SERVIÇOS DE VAREJO S.A.
   CNPJ: 15436940000172
   
2. AMAZON WEB SERVICES BRASIL SERVIÇOS DE COMPUTAÇÃO EM NUVEM LTDA.
   CNPJ: 15633122000156
   
...
```

---

### 4. Processar Arquivo CSV

```bash
python cli/cnpj_cli.py --csv lista_cnpjs.csv --output resultado.json
```

**Formato esperado (lista_cnpjs.csv):**
```
cnpj
11222333000181
15436940000172
15633122000156
```

**Saída (resultado.json):**
```json
[
  {
    "cnpj": "11222333000181",
    "razao_social": "...",
    "status": "sucesso"
  },
  ...
]
```

---

### 5. Exportar para Diferentes Formatos

```bash
# JSON
python cli/cnpj_cli.py --cnpj 11222333000181 --format json

# CSV
python cli/cnpj_cli.py --cnpj 11222333000181 --format csv

# XML
python cli/cnpj_cli.py --cnpj 11222333000181 --format xml

# Tabela (terminal)
python cli/cnpj_cli.py --cnpj 11222333000181 --format table
```

---

## Opções Avançadas

### Cache Local

```bash
# Ativar cache
python cli/cnpj_cli.py --cnpj 11222333000181 --cache

# Limpar cache
python cli/cnpj_cli.py --clear-cache

# Ver cache
python cli/cnpj_cli.py --cache-info
```

---

### Configurar Fonte de Dados

```bash
# Usar BrasilAPI (padrão)
python cli/cnpj_cli.py --cnpj 11222333000181 --source brasilapi

# Usar Receita Federal (offline, mais dados)
python cli/cnpj_cli.py --cnpj 11222333000181 --source receita-federal

# Usar Serenata (com análise)
python cli/cnpj_cli.py --cnpj 11222333000181 --source serenata
```

---

### Processamento em Batch

```bash
# Processar 100 CNPJs com paralelização
python cli/cnpj_cli.py --csv grande_lista.csv --parallel --workers 4

# Ver progresso
python cli/cnpj_cli.py --csv lista.csv --verbose
```

---

### Filtrar Resultados

```bash
# Apenas empresas ativas
python cli/cnpj_cli.py --search "Empresa" --status "ATIVA"

# Apenas na região Sudeste
python cli/cnpj_cli.py --search "Empresa" --region "sudeste"

# Por tipo jurídico
python cli/cnpj_cli.py --search "Empresa" --tipo "SA"
```

---

## Exemplos Prácticos

### Exemplo 1: Validar e Salvar
```bash
python cli/cnpj_cli.py \
  --cnpj 11222333000181 \
  --output dados_empresa.json \
  --format json
```

### Exemplo 2: Busca com Filtros
```bash
python cli/cnpj_cli.py \
  --search "Tech" \
  --region "sudeste" \
  --status "ATIVA" \
  --limit 50 \
  --output empresas_tech.csv
```

### Exemplo 3: Processamento em Lote
```bash
python cli/cnpj_cli.py \
  --csv lista_clientes.csv \
  --parallel \
  --workers 8 \
  --output clientes_enriquecidos.json \
  --cache
```

### Exemplo 4: Monitor em Tempo Real
```bash
python cli/cnpj_cli.py \
  --monitor \
  --watch lista.csv \
  --interval 60
```

---

## Configuração

Arquivo: `cli/config.yaml`

```yaml
# Fonte de dados padrão
default_source: brasilapi

# Cache
cache:
  enabled: true
  ttl: 86400  # 24 horas

# Paralelização
parallel:
  enabled: true
  workers: 4

# Rate limiting
rate_limit:
  requests_per_second: 10
  
# Logging
logging:
  level: INFO
  file: cnpj_explorer.log
```

---

## Variáveis de Ambiente

```bash
# API Keys (se necessário)
export BRASILAPI_KEY="sua_chave"
export RECEITA_FEDERAL_KEY="sua_chave"

# Configurações
export CNPJ_CACHE_DIR="/caminho/para/cache"
export CNPJ_LOG_LEVEL="DEBUG"
export CNPJ_WORKERS=8

# Então usar:
python cli/cnpj_cli.py --cnpj 11222333000181
```

---

## Troubleshooting

### Erro: "Connection refused"
```bash
# Verificar se BrasilAPI está acessível
curl https://brasilapi.com.br/api/cnpj/v1/11222333000181
```

### Erro: "Rate limit exceeded"
```bash
# Aumentar delay
python cli/cnpj_cli.py --cnpj ... --delay 2

# Ou usar Receita Federal (offline)
python cli/cnpj_cli.py --cnpj ... --source receita-federal
```

### Erro: "Cache corrupted"
```bash
# Limpar cache
python cli/cnpj_cli.py --clear-cache

# Recomeçar
python cli/cnpj_cli.py --cnpj ...
```

---

## Próximas Versões

- [ ] Integração com banco de dados (SQLite/PostgreSQL)
- [ ] Webhook para notificações
- [ ] API REST própria
- [ ] Dashboard web
- [ ] Mobile app

---

**Última atualização:** 2026-09-09
