# 📊 CNPJ Skill - Documentação Completa

Skill integrada que unifica todas as soluções de consulta de CNPJ em um único comando.

## 🚀 Instalação Rápida

```bash
chmod +x ~/Claude_CLI/create-skill/cnpj-skill-config.sh
~/Claude_CLI/create-skill/cnpj-skill-config.sh
```

Depois você pode usar diretamente:
```bash
cnpj-skill --help
```

## 📋 Comandos Principais

### Consulta Simples
```bash
# Com validação automática
cnpj-skill --cnpj 11222333000181

# Resultado formatado
cnpj-skill --cnpj 11222333000181 | jq .
```

### Validação
```bash
# Validar sem consultar
cnpj-skill --validate 11.222.333/0001-81
cnpj-skill --validate 11222333000181

# Retorna: ✓ (válido) ou ✗ (inválido)
```

### Diferentes APIs

**BrasilAPI (Recomendado - Gratuita e Rápida)**
```bash
cnpj-skill --brasilapi 11222333000181
# Resposta em ~500ms
# Dados básicos: razão social, CNAE, situação cadastral
```

**Receita Federal (Completo - Mais Lento)**
```bash
cnpj-skill --receita 11222333000181
# Requer dataset (~1GB na primeira vez)
# Dados completos: sócios, atividades, histórico
```

### Processamento em Lote
```bash
# Arquivo com CNPJs, 1 por linha
cat empresas.txt
# 11222333000181
# 34028316000172
# 07526847000148

# Processar
cnpj-skill --batch empresas.txt

# Resultado em: ~/.cache/cnpj-skill/batch_resultado_*.json
```

### Exportar para Excel
```bash
cnpj-skill --brasilapi 11222333000181 --export dados.xlsx

# Gera arquivo com formatação automática
```

### Gerenciar Cache
```bash
# Ver arquivos em cache
cnpj-skill --cache list

# Estatísticas
cnpj-skill --cache stats

# Limpar cache
cnpj-skill --cache clear
```

## 📊 Tipos de Dados Retornados

### BrasilAPI

```json
{
  "cnpj": "11222333000181",
  "razao_social": "NOME DA EMPRESA LTDA",
  "cnae_fiscal": "1234-5/67",
  "descricao_cnae_fiscal": "Atividade econômica",
  "natureza_juridica": "2062",
  "descricao_natureza_juridica": "Sociedade Limitada",
  "logradouro": "RUA EXEMPLO",
  "numero": "123",
  "complemento": "APTO 456",
  "bairro": "CENTRO",
  "municipio": "SAO PAULO",
  "uf": "SP",
  "cep": "01234567",
  "telefone": "1133334444",
  "email": "contato@empresa.com.br",
  "situacao_cadastral": "ATIVA",
  "data_situacao_cadastral": "2020-01-15",
  "motivo_situacao_cadastral": "Sem motivo",
  "nome_fantasia": "NOME FANTASIA",
  "data_inicio_atividade": "2005-03-20",
  "cnae_fiscal_descricao": "Comércio varejista",
  "descricao_tipo_logradouro": "Rua",
  "correios_endereco_formatado": "RUA EXEMPLO 123"
}
```

### Receita Federal (mais completo)
- Informações de sócios
- Histórico de alterações
- Atividades econômicas completas
- Informações de inscrição estadual
- Dados de faturamento

## 🔄 Exemplos de Uso

### 1. Validar lista de CNPJs
```bash
for cnpj in 11222333000181 34028316000172 99999999999999; do
    if cnpj-skill --validate "$cnpj" 2>/dev/null; then
        echo "✓ $cnpj válido"
    else
        echo "✗ $cnpj inválido"
    fi
done
```

### 2. Consultar e salvar em JSON
```bash
cnpj-skill --cnpj 11222333000181 > empresa.json
cat empresa.json | jq '.razao_social'
```

### 3. Processar múltiplas empresas com relatório
```bash
cnpj-skill --batch empresas.txt > relatorio.json

# Análise com jq
cat relatorio.json | jq '.[] | {cnpj, razao_social, uf}' > resumo.json
```

### 4. Integrar em scripts
```bash
#!/bin/bash

CNPJ="11222333000181"

if cnpj-skill --validate "$CNPJ"; then
    DATA=$(cnpj-skill --cnpj "$CNPJ")
    EMPRESA=$(echo "$DATA" | jq -r '.razao_social')
    echo "Empresa: $EMPRESA"
else
    echo "CNPJ inválido"
    exit 1
fi
```

### 5. Usar em Python
```python
import subprocess
import json

cnpj = "11222333000181"

# Executar skill
result = subprocess.run(
    ["cnpj-skill", "--cnpj", cnpj],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    dados = json.loads(result.stdout)
    print(f"Empresa: {dados['razao_social']}")
else:
    print(f"Erro: {result.stderr}")
```

## 📁 Estrutura de Arquivos

```
~/.cache/cnpj-skill/
├── brasilapi_11222333000181.json    # Cache de consultadas
└── batch_resultado_1694274842.json

~/.local/share/cnpj-skill/
└── cnpj-skill.log                   # Arquivo de log

~/.config/cnpj-skill/
└── config.env                       # Configurações

~/Claude_CLI/bin/
└── cnpj-skill                       # Binário principal

~/Claude_CLI/cnpj-explorer/
├── cli/
├── apis/
├── examples/
└── docs/
```

## ⚙️ Configuração Avançada

### Editar arquivo de configuração
```bash
nano ~/.config/cnpj-skill/config.env
```

Opções:
- `CACHE_ENABLED`: true/false
- `CACHE_TTL`: Segundos até expirar cache (padrão: 86400)
- `DEFAULT_API`: brasilapi ou receita
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR

### Usar API customizada
```bash
# Editar ~/.config/cnpj-skill/config.env
BRASILAPI_URL=https://sua-api.com/v1/
```

## 🔍 Resolução de Problemas

### "command not found: cnpj-skill"
```bash
# Verificar se foi instalado
ls -la ~/Claude_CLI/bin/cnpj-skill

# Executar script de instalação
bash ~/Claude_CLI/create-skill/cnpj-skill-config.sh

# Adicionar ao PATH se necessário
echo 'export PATH="$HOME/Claude_CLI/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "CNPJ não encontrado"
- Verifique se o CNPJ está correto (sem formatação ou com formatação correta)
- A API BrasilAPI pode não ter dados de todos os CNPJs
- Tente com `--receita` para dados mais completos

### "curl: command not found"
```bash
# Instalar curl
brew install curl  # macOS
apt install curl   # Linux
```

### Cache corrompido
```bash
cnpj-skill --cache clear
```

## 📈 Performance

| Operação | Tempo | Notas |
|----------|-------|-------|
| Consulta simples | ~500ms | Com cache: <10ms |
| Lote (10 CNPJs) | ~5s | Em paralelo: ~2s |
| Validação | ~50ms | Local, sem rede |
| Export Excel | ~2s | Gera arquivo formatado |

## 🔒 Privacidade e Segurança

- Dados são consultados de APIs públicas
- Cache é armazenado localmente (não sincronizado)
- Nenhum dado sensível é enviado para terceiros
- Logs não incluem CNPJs (apenas operações)

## 📞 Próximas Melhorias

- [ ] Suporte a CPF
- [ ] Análise de relacionamentos (sócios)
- [ ] Alertas de situação cadastral
- [ ] Integração com webhook
- [ ] Modo daemon para monitoramento
- [ ] Dashboard web

## 📚 Referências

- [BrasilAPI Docs](https://brasilapi.com.br)
- [Receita Federal Dados Públicos](https://www.gov.br/cidadania/pt-br)
- [Projeto CNPJ Explorer](../cnpj-explorer)

---

**Versão:** 1.0.0  
**Última atualização:** 2026-09-09  
**Criador:** Claude Code
