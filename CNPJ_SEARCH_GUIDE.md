# 🔍 Guia: Pesquisa Automática de CNPJ + LinkedIn

## Opção 1: Usar o Script Python

```bash
python3 search_cnpj_linkedin.py 28.015.659/0001-30
```

**Ou com sócios específicos:**
```bash
python3 search_cnpj_linkedin.py 28.015.659/0001-30 "Luis de Mattos" "Maria Alice"
```

---

## Opção 2: Usar o Script Bash (Shell)

```bash
bash ~/.claude/projects/-Users-thiago-dias/skills/cnpj-search.sh 28.015.659/0001-30
```

**Ou com sócios:**
```bash
bash ~/.claude/projects/-Users-thiago-dias/skills/cnpj-search.sh 28.015.659/0001-30 "Luis de Mattos" "Maria Alice"
```

---

## Opção 3: Criar um Alias (Recomendado)

Adicione ao seu `~/.zshrc`:

```bash
alias cnpj-search='bash ~/.claude/projects/-Users-thiago-dias/skills/cnpj-search.sh'
```

Depois use:
```bash
cnpj-search 28.015.659/0001-30
```

---

## Opção 4: Usar com Claude Code Hook

Para automatizar **sempre que você digita um CNPJ**, adicione este hook em `.claude/settings.json`:

```json
{
  "hooks": {
    "after-submit": {
      "command": "bash ~/.claude/projects/-Users-thiago-dias/skills/cnpj-search.sh",
      "args": ["$USER_INPUT"],
      "condition": "matches(\"[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}\")"
    }
  }
}
```

---

## 📊 Queries de Busca Automáticas

Quando você executa qualquer dessas opções, o script gera automaticamente:

### 1. Busca de Informações Gerais
```
rtk web search "28.015.659/0001-30" OR "28015659000130" empresa
```

### 2. Busca em Plataformas CNPJ
```
rtk web fetch "https://casadosdados.com.br/solucao/cnpj/28.015.659/0001-30"
```

### 3. Busca de Sócios no LinkedIn
```
rtk web search "Luis de Mattos" site:linkedin.com
rtk web search "Maria Alice Araujo de Mattos" site:linkedin.com
rtk web search "Guilherme Maranhao Gobbi Silva" site:linkedin.com
```

---

## 💰 Economia com RTK

Todas as pesquisas usam `rtk` para economizar **60-90% de tokens**:

```bash
rtk gain              # Ver economias acumuladas
rtk gain --history    # Ver histórico de comandos com economia
```

---

## 🎯 Exemplo Completo: Pesquisar CNPJ

```bash
$ cnpj-search 28.015.659/0001-30

╔════════════════════════════════════════════════════════════╗
║        🔎 PESQUISADOR DE CNPJ + LINKEDIN                  ║
╚════════════════════════════════════════════════════════════╝

📋 CNPJ: 28.015.659/0001-30
📊 CNPJ (sem formatação): 28015659000130

🔍 QUERIES DE BUSCA GERADAS:

1️⃣  Informações gerais do CNPJ:
   rtk web search "28.015.659/0001-30" OR "28015659000130" empresa

2️⃣  Busca em plataformas CNPJ:
   rtk web fetch "https://casadosdados.com.br/solucao/cnpj/28.015.659/0001-30"

3️⃣  Busca de sócios no LinkedIn:
   rtk web search "sócios" "28.015.659/0001-30" site:linkedin.com
   rtk web search "administrador" "28.015.659/0001-30" site:linkedin.com

⚡ Para economizar tokens, use RTK:
   rtk gain  # ver economias
```

---

## 🔗 Integração com Claude Code

Para que Claude sempre execute isso automaticamente, adicione em `/Users/thiago.dias/.claude/projects/-Users-thiago-dias/.claude/settings.json`:

```json
{
  "triggers": {
    "cnpj_pattern": {
      "regex": "[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}",
      "action": "run_skill",
      "skill": "cnpj-search",
      "auto_continue": true
    }
  }
}
```

---

**Pronto!** Agora você tem uma pesquisa automática de CNPJ + LinkedIn integrada! 🚀
