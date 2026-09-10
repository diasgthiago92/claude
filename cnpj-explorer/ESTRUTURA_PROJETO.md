# 📁 Estrutura do Projeto CNPJ Explorer

Visão geral completa da organização do projeto.

---

## 🎯 Organização de Diretórios

```
cnpj-explorer/
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md                    # Visão geral (leia isto primeiro!)
│   ├── QUICKSTART.md                # Começar em 5 minutos
│   ├── ESTRUTURA_PROJETO.md         # Este arquivo
│   └── docs/
│       ├── REPOSITORIOS_GITHUB.md   # Repos prontos para usar
│       ├── CLI.md                   # Guia completo da CLI
│       ├── INTEGRACAO_APIS.md       # Como integrar APIs
│       └── COMPARACAO.md            # Qual solução usar
│
├── 🖥️  CLI & SCRIPTS
│   └── cli/
│       └── cnpj_cli.py              # Interface de linha de comando
│
├── 💻 CÓDIGO & EXEMPLOS
│   └── examples/
│       ├── validate_cnpj.py         # Validação básica
│       ├── brasilapi_integration.py # Integração BrasilAPI
│       └── batch_processing.py      # Processamento em lote
│
├── ⚙️  CONFIGURAÇÃO
│   ├── requirements.txt             # Dependências Python
│   ├── .env.example                 # Variáveis de ambiente (exemplo)
│   ├── install.sh                   # Script de instalação
│   └── .gitignore                   # Configuração Git
│
├── 📂 DIRETÓRIOS CRIADOS NA INSTALAÇÃO
│   ├── venv/                        # Ambiente virtual Python
│   ├── cache/                       # Cache local de CNPJs
│   ├── data/                        # Dados baixados
│   ├── logs/                        # Logs da aplicação
│   └── output/                      # Resultados exportados
│
└── 📋 ARQUIVOS DE CONFIGURAÇÃO
    └── .env                         # Configurações (criado durante instalação)
```

---

## 📖 Qual Documento Ler?

### Se você quer...

**✅ Começar rápido (5 min)**
→ [QUICKSTART.md](./QUICKSTART.md)

**✅ Entender todas as opções**
→ [README.md](./README.md)

**✅ Ver repositórios prontos no GitHub**
→ [docs/REPOSITORIOS_GITHUB.md](./docs/REPOSITORIOS_GITHUB.md)

**✅ Usar a CLI própria**
→ [docs/CLI.md](./docs/CLI.md)

**✅ Integrar APIs em seu código**
→ [docs/INTEGRACAO_APIS.md](./docs/INTEGRACAO_APIS.md)

**✅ Decidir qual solução usar**
→ [docs/COMPARACAO.md](./docs/COMPARACAO.md)

---

## 🚀 Como Usar

### 1️⃣ Instalação
```bash
cd /Users/thiago.dias/Claude_CLI/cnpj-explorer
chmod +x install.sh
./install.sh
source venv/bin/activate
```

### 2️⃣ Verificar Instalação
```bash
# Validar um CNPJ
python cli/cnpj_cli.py --validate 15436940000172

# Buscar informações
python cli/cnpj_cli.py --cnpj 15436940000172
```

### 3️⃣ Escolher sua abordagem

**Opção A: Usar CLI próprio (recomendado)**
```bash
python cli/cnpj_cli.py --csv dados.csv --output resultado.json --parallel
```

**Opção B: Usar exemplos de código**
```bash
python examples/brasilapi_integration.py
python examples/batch_processing.py
```

**Opção C: Usar repositório externo**
- Veja [REPOSITORIOS_GITHUB.md](./docs/REPOSITORIOS_GITHUB.md)

---

## 📊 Opções Disponíveis

### Opção 1: BrasilAPI (Recomendada)
- **Quanto:** Gratuita
- **Dados:** Básicos + suficientes
- **Instalação:** Imediata
- **Como:** `python cli/cnpj_cli.py --cnpj ...`

### Opção 2: CLI Próprio Customizado
- **Quanto:** Gratuita
- **Dados:** Configurável
- **Instalação:** 5-10 min
- **Como:** Editar `cli/cnpj_cli.py`

### Opção 3: Receita Federal (Offline)
- **Quanto:** Gratuita
- **Dados:** Completos
- **Instalação:** 1-2 horas
- **Como:** Baixar + processar dados

### Opção 4: Serenata (Análise)
- **Quanto:** Gratuita
- **Dados:** Com análise
- **Instalação:** 15 min
- **Como:** `pip install serenata-toolbelt`

### Opção 5: Repositório GitHub Externo
- **Quanto:** Varia
- **Dados:** Completos
- **Instalação:** Varia
- **Como:** Clonar repo (veja docs)

---

## 🔧 Arquivos Importantes

### `cli/cnpj_cli.py` (150 linhas)
Interface de linha de comando pronta para usar.

**Usar:**
```bash
python cli/cnpj_cli.py --help
python cli/cnpj_cli.py --cnpj 15436940000172
python cli/cnpj_cli.py --csv dados.csv --output resultado.json
```

### `examples/brasilapi_integration.py` (200 linhas)
Classe `BuscadorBrasilAPI` com cache e tratamento de erros.

**Usar:**
```python
from examples.brasilapi_integration import BuscadorBrasilAPI

api = BuscadorBrasilAPI()
dados = api.buscar("15436940000172")
```

### `examples/batch_processing.py` (250 linhas)
Classe `ProcessadorBatch` para processar muitos CNPJs em paralelo.

**Usar:**
```python
from examples.batch_processing import ProcessadorBatch

p = ProcessadorBatch(max_workers=8)
p.processar_csv("entrada.csv", "saida.json", paralelo=True)
```

### `examples/validate_cnpj.py` (80 linhas)
Funções para validação e formatação.

**Usar:**
```python
from examples.validate_cnpj import validar_cnpj, formatar_cnpj

validar_cnpj("15436940000172")      # True/False
formatar_cnpj("15436940000172")     # "15.436.940/0001-72"
```

---

## 🎓 Fluxos de Trabalho Comuns

### Workflow 1: Validar CNPJs
```bash
python cli/cnpj_cli.py --validate 15436940000172
python cli/cnpj_cli.py --validate 11222333000181
```

### Workflow 2: Buscar um CNPJ
```bash
python cli/cnpj_cli.py --cnpj 15436940000172 --format table
```

### Workflow 3: Processar arquivo
```bash
python cli/cnpj_cli.py --csv clientes.csv --output clientes_dados.json --cache
```

### Workflow 4: Processar em paralelo (rápido)
```bash
python cli/cnpj_cli.py --csv grandes_clientes.csv \
  --output resultado.json \
  --parallel \
  --workers 8
```

### Workflow 5: Personalizar código
```python
# Editar examples/brasilapi_integration.py
# Adicionar suas lógicas
# Usar em seu projeto
```

---

## 💡 Casos de Uso

| Caso | Solução |
|------|---------|
| Validar 1-2 CNPJs | `cli/cnpj_cli.py --validate` |
| Buscar dados de 1 CNPJ | `cli/cnpj_cli.py --cnpj` |
| Processar 100 CNPJs | `cli/cnpj_cli.py --csv ... --output` |
| Processar 10k CNPJs | `cli/cnpj_cli.py --csv ... --parallel` |
| Integrar em seu código | Copiar `examples/*.py` |
| Dados offline | Usar Receita Federal |
| Análise de integridade | Serenata |
| Máxima precisão | Meu CNPJ (pago) |

---

## 🔄 Próximas Melhorias

Essas funcionalidades podem ser adicionadas:

- [ ] Dashboard web
- [ ] Banco de dados integrado (SQLite/PostgreSQL)
- [ ] API REST própria
- [ ] WebHooks para notificações
- [ ] Integração com Serenata automática
- [ ] Relatórios PDF
- [ ] Monitoramento de mudanças em CNPJs

---

## 📞 Suporte

### Problemas Comuns

**"Connection refused"**
- BrasilAPI pode estar offline
- Verificar: `curl https://brasilapi.com.br/api/cnpj/v1/15436940000172`
- Alternativa: Usar Receita Federal

**"Rate limit exceeded"**
- BrasilAPI tem limite de 50 req/min
- Aguarde ou use Receita Federal

**"ModuleNotFoundError"**
- Execute: `pip install -r requirements.txt`

### Documentação Adicional

- [README.md](./README.md) - Visão geral
- [QUICKSTART.md](./QUICKSTART.md) - Começar rápido
- [docs/](./docs/) - Documentação completa

---

## 🎯 Recomendações

1. **Para começar:** Use [QUICKSTART.md](./QUICKSTART.md) (5 min)
2. **Para integrar:** Use `examples/brasilapi_integration.py`
3. **Para processar muitos:** Use `cli/cnpj_cli.py --parallel`
4. **Para customizar:** Copie exemplos e adapte
5. **Para produção:** Veja [docs/COMPARACAO.md](./docs/COMPARACAO.md)

---

**Última atualização:** 2026-09-09
**Versão:** 1.0.0
