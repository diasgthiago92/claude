# 🚀 Quick Start - CNPJ Explorer

Comece em **5 minutos** com as opções prontas para usar.

---

## 📦 Instalação Rápida

```bash
cd /Users/thiago.dias/Claude_CLI/cnpj-explorer
chmod +x install.sh
./install.sh

# Ativar ambiente
source venv/bin/activate
```

---

## 🎯 3 Opções Imediatas

### Opção 1: Validar CNPJ (Mais Simples)

```bash
python cli/cnpj_cli.py --validate 15436940000172
```

**Output:**
```
✅ CNPJ válido
   Formatado: 15.436.940/0001-72
```

---

### Opção 2: Consultar BrasilAPI (Recomendado)

```bash
# Buscar um CNPJ
python cli/cnpj_cli.py --cnpj 15436940000172

# Ver em formato tabela
python cli/cnpj_cli.py --cnpj 15436940000172 --format table
```

**Output:**
```json
{
  "cnpj": "15436940000172",
  "razao_social": "AMAZON BRASIL SERVIÇOS DE VAREJO S.A.",
  "logradouro": "AV BRASIL",
  "numero": "2000",
  "municipio": "SAO PAULO",
  "uf": "SP",
  "cep": "08000000"
}
```

---

### Opção 3: Processar Arquivo CSV

```bash
# Criar arquivo de teste
echo "cnpj" > meus_cnpjs.csv
echo "15436940000172" >> meus_cnpjs.csv
echo "15633122000156" >> meus_cnpjs.csv

# Processar
python cli/cnpj_cli.py --csv meus_cnpjs.csv --output resultado.json

# Ver resultado
cat output/resultado.json
```

---

## 🔥 10 Exemplos Práticos

### 1. Validar CNPJ Simples
```bash
python cli/cnpj_cli.py --validate 11222333000181
```

### 2. Buscar Formatar CNPJ
```bash
python cli/cnpj_cli.py --cnpj 11222333000181 --format table
```

### 3. Exportar como CSV
```bash
python cli/cnpj_cli.py --cnpj 15436940000172 --format csv
```

### 4. Processar Múltiplos CNPJs (Sequencial)
```bash
python cli/cnpj_cli.py --csv lista.csv --output resultado.json
```

### 5. Processar com Paralelização (Mais Rápido)
```bash
python cli/cnpj_cli.py --csv lista.csv --output resultado.json --parallel --workers 8
```

### 6. Com Cache (Reutilizar Dados)
```bash
python cli/cnpj_cli.py --cnpj 15436940000172 --cache
python cli/cnpj_cli.py --cnpj 15436940000172 --cache  # Segunda é instantânea
```

### 7. Ver Cache Ativo
```bash
python cli/cnpj_cli.py --cache-info
```

### 8. Limpar Cache
```bash
python cli/cnpj_cli.py --clear-cache
```

### 9. Executar Exemplo Completo (BrasilAPI)
```bash
python examples/brasilapi_integration.py
```

### 10. Processar Lote Grande (Batch)
```bash
python examples/batch_processing.py
```

---

## 📚 Documentação Completa

| Documento | Conteúdo |
|-----------|----------|
| [README.md](./README.md) | Visão geral completa |
| [REPOSITORIOS_GITHUB.md](./docs/REPOSITORIOS_GITHUB.md) | Repos prontos para usar |
| [CLI.md](./docs/CLI.md) | Todas as opções da CLI |
| [INTEGRACAO_APIS.md](./docs/INTEGRACAO_APIS.md) | Como integrar APIs |
| [COMPARACAO.md](./docs/COMPARACAO.md) | Qual solução usar |

---

## 🎓 Exemplos de Código

| Arquivo | Propósito |
|---------|----------|
| [validate_cnpj.py](./examples/validate_cnpj.py) | Validação básica |
| [brasilapi_integration.py](./examples/brasilapi_integration.py) | Integrar com BrasilAPI |
| [batch_processing.py](./examples/batch_processing.py) | Processar em lote |

---

## 🔗 Links Úteis

- **BrasilAPI:** https://brasilapi.com.br/
- **Receita Federal:** https://www.gov.br/pt-br/servicos/consultar-dados-cadastrais-da-empresa
- **Serenata:** https://github.com/serenata/serenata-de-amor

---

## ⚡ Dicas de Performance

1. **Use cache** para CNPJs repetidos
```bash
python cli/cnpj_cli.py --cnpj ... --cache
```

2. **Use paralelização** para listas grandes
```bash
python cli/cnpj_cli.py --csv grande_lista.csv --parallel --workers 8
```

3. **Considere Receita Federal** para offline
- Download inicial (~100MB)
- Depois consulta local (muito rápido)

4. **Combine fontes** para melhor resultado
- BrasilAPI para começar
- Fallback para Receita Federal
- Análise com Serenata

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install -r requirements.txt
```

### "Connection refused" (BrasilAPI offline)
```bash
# Verificar se API está acessível
curl https://brasilapi.com.br/api/cnpj/v1/15436940000172

# Se não funcionar, usar Receita Federal (offline)
```

### "Rate limit exceeded"
```bash
# Esperar um pouco e tentar novamente
# Ou usar Receita Federal (sem rate limit)
```

---

## 🚀 Próximos Passos

1. **Escolher sua solução** → Ler [COMPARACAO.md](./docs/COMPARACAO.md)
2. **Entender as opções** → Ler [REPOSITORIOS_GITHUB.md](./docs/REPOSITORIOS_GITHUB.md)
3. **Integrar em seu código** → Ler [INTEGRACAO_APIS.md](./docs/INTEGRACAO_APIS.md)
4. **Usar a CLI** → `python cli/cnpj_cli.py --help`

---

**Última atualização:** 2026-09-09
**Versão:** 1.0.0
