# Backup Automático Claude_CLI

Sincronização automática diária de `Claude_CLI` para `https://github.com/diasgthiago92/claude` às **16:00**.

## 📋 Componentes

1. **Script de Backup**: `bin/backup.sh`
   - Sincroniza Claude_CLI com repositório GitHub
   - Faz commit e push automático
   - Registra logs em `logs/backup_*.log`

2. **Configuração LaunchD**: `settings/com.claude.backup.plist`
   - Daemon do macOS que executa o script diariamente
   - Agendado para rodar às 16:00
   - Redireciona stdout/stderr para arquivos de log

## ⚙️ Instalação

### Passo 1: Clonar o plist para LaunchAgents

```bash
cp /Users/thiago.dias/Claude_CLI/settings/com.claude.backup.plist \
   ~/Library/LaunchAgents/com.claude.backup.plist
```

### Passo 2: Carregar o agente

```bash
launchctl load ~/Library/LaunchAgents/com.claude.backup.plist
```

### Passo 3: Verificar se está ativo

```bash
launchctl list | grep com.claude.backup
```

## 🧪 Testes

### Executar backup manualmente
```bash
/Users/thiago.dias/Claude_CLI/bin/backup.sh
```

### Forçar execução imediata do launchd
```bash
launchctl start com.claude.backup
```

### Ver logs
```bash
tail -f /Users/thiago.dias/Claude_CLI/logs/backup.stdout.log
tail -f /Users/thiago.dias/Claude_CLI/logs/backup.stderr.log
```

## 🔧 Gerenciamento

### Desativar temporariamente
```bash
launchctl unload ~/Library/LaunchAgents/com.claude.backup.plist
```

### Reativar
```bash
launchctl load ~/Library/LaunchAgents/com.claude.backup.plist
```

### Remover completamente
```bash
launchctl unload ~/Library/LaunchAgents/com.claude.backup.plist
rm ~/Library/LaunchAgents/com.claude.backup.plist
```

## 📝 Variáveis do Script

- `CLAUDE_CLI_PATH`: Caminho da pasta Claude_CLI
- `GITHUB_REPO`: URL do repositório GitHub
- `TIMESTAMP`: Data/hora do backup
- `LOG_FILE`: Arquivo de log do backup

## 🚫 Exclusões

O script não sincroniza:
- `.git/` - histórico Git
- `.kirocrew.breadcrumb` - marcador de identidade
- `venv/` - ambiente virtual Python
- `__pycache__/` - cache Python
- `.pytest_cache/` - cache de testes
- `node_modules/` - dependências Node

## 🔑 Autenticação GitHub

O script usa credenciais do git configuradas localmente. Certifique-se de:

1. Ter acesso SSH ao repositório:
   ```bash
   ssh -T git@github.com
   ```

2. OU ter PAT (Personal Access Token) configurado:
   ```bash
   git config --global credential.helper osxkeychain
   ```

## 📊 Monitoramento

Verifique regularmente:
- `logs/backup_*.log` - histórico de backups
- GitHub repository - confirmação de pushes
- `launchctl list | grep com.claude.backup` - status do daemon
