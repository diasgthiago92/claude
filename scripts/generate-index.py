#!/usr/bin/env python3
"""
Gerador de Índice do Claude CLI
Mapeia: Settings, Skills, Rotinas, Agentes, MCP Servers
"""

import json
import os
from pathlib import Path
from datetime import datetime

HOME = Path.home()
CLAUDE_CLI = HOME / "Claude_CLI"
CLAUDE_CONFIG = HOME / ".claude"

def scan_settings():
    """Escaneia configurações do Claude"""
    settings = {}

    # settings.json global
    global_settings = CLAUDE_CONFIG / "settings.json"
    if global_settings.exists():
        with open(global_settings) as f:
            settings["global"] = json.load(f)

    # settings.local.json
    local_settings = CLAUDE_CONFIG / "settings.local.json"
    if local_settings.exists():
        with open(local_settings) as f:
            settings["local"] = json.load(f)

    return settings

def scan_skills():
    """Lista skills instaladas"""
    skills_dir = CLAUDE_CONFIG / "skills"
    skills = []

    if skills_dir.exists():
        for skill_file in skills_dir.glob("*.md"):
            skills.append({
                "name": skill_file.stem,
                "path": str(skill_file),
                "type": "skill"
            })

    return skills

def scan_mcp_servers():
    """Lista servidores MCP configurados"""
    settings_file = CLAUDE_CONFIG / "settings.json"
    mcp_servers = []

    if settings_file.exists():
        with open(settings_file) as f:
            settings = json.load(f)
            if "mcpServers" in settings:
                for name, config in settings["mcpServers"].items():
                    mcp_servers.append({
                        "name": name,
                        "command": config.get("command"),
                        "args": config.get("args", []),
                        "disabled": config.get("disabled", False),
                        "type": "mcp"
                    })

    return mcp_servers

def scan_claude_cli_structure():
    """Mapeia estrutura do Claude_CLI"""
    structure = {
        "scripts": [],
        "mcp": [],
        "analises": [],
        "memoria": [],
        "outros": []
    }

    if CLAUDE_CLI.exists():
        # Scripts
        scripts_dir = CLAUDE_CLI / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*"):
                if script.is_file() and (script.suffix in [".py", ".sh", ".js"]):
                    structure["scripts"].append({
                        "name": script.name,
                        "path": str(script),
                        "type": "script"
                    })

        # MCP
        mcp_dir = CLAUDE_CLI / "mcp"
        if mcp_dir.exists():
            for file in mcp_dir.glob("*.js"):
                structure["mcp"].append({
                    "name": file.name,
                    "path": str(file),
                    "type": "mcp_server"
                })

        # Análises
        analises_dir = CLAUDE_CLI / "Análises"
        if analises_dir.exists():
            for proj in analises_dir.iterdir():
                if proj.is_dir():
                    structure["analises"].append({
                        "name": proj.name,
                        "path": str(proj),
                        "type": "project"
                    })

        # Memória
        memoria_dir = CLAUDE_CONFIG / "projects/-Users-thiago-dias/memory"
        if memoria_dir.exists():
            for mem in memoria_dir.glob("*.md"):
                structure["memoria"].append({
                    "name": mem.stem,
                    "path": str(mem),
                    "type": "memory"
                })

    return structure

def generate_markdown_index():
    """Gera índice em Markdown"""

    settings = scan_settings()
    skills = scan_skills()
    mcp_servers = scan_mcp_servers()
    structure = scan_claude_cli_structure()

    md = []
    md.append("# 📚 Índice Completo - Claude CLI\n")
    md.append(f"**Atualizado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    md.append("---\n")

    # 1. Settings
    md.append("## ⚙️ Settings & Configurações\n")
    if settings:
        if "global" in settings:
            md.append("### Global Settings (`~/.claude/settings.json`)\n")
            md.append("```json\n")
            md.append(json.dumps(settings["global"], indent=2, ensure_ascii=False)[:500])
            md.append("\n...\n```\n")

        if "local" in settings:
            md.append("### Local Settings (`~/.claude/settings.local.json`)\n")
            md.append("Configurações locais ativadas ✅\n")
    md.append("\n")

    # 2. MCP Servers
    md.append("## 🔗 MCP Servers (Integrações)\n")
    if mcp_servers:
        for server in mcp_servers:
            status = "❌ Desativado" if server["disabled"] else "✅ Ativo"
            md.append(f"### {server['name']} {status}\n")
            md.append(f"- **Command:** `{server['command']}`\n")
            if server['args']:
                md.append(f"- **Args:** {' '.join(server['args'][:1])}...\n")
            md.append("\n")
    else:
        md.append("Nenhum MCP server configurado\n\n")

    # 3. Skills
    md.append("## 🎯 Skills Disponíveis\n")
    if skills:
        for skill in skills:
            md.append(f"- **{skill['name']}** → `{skill['path']}`\n")
    else:
        md.append("Nenhuma skill encontrada\n")
    md.append("\n")

    # 4. Estrutura Claude_CLI
    md.append("## 📁 Estrutura Claude_CLI\n")

    if structure["scripts"]:
        md.append("### Scripts Python/Shell\n")
        for script in structure["scripts"]:
            md.append(f"- `{script['name']}`\n")
        md.append("\n")

    if structure["mcp"]:
        md.append("### MCP Servers\n")
        for server in structure["mcp"]:
            md.append(f"- `{server['name']}`\n")
        md.append("\n")

    if structure["analises"]:
        md.append("### Projetos/Análises\n")
        for proj in structure["analises"]:
            md.append(f"- **{proj['name']}**\n")
        md.append("\n")

    if structure["memoria"]:
        md.append("### Memória Persistente\n")
        for mem in structure["memoria"][:10]:  # Primeiras 10
            md.append(f"- {mem['name']}\n")
        if len(structure["memoria"]) > 10:
            md.append(f"- ... e {len(structure['memoria']) - 10} mais\n")
        md.append("\n")

    # 5. Rotinas
    md.append("## ⏰ Rotinas & Agendamentos\n")
    md.append("### Verificar com:\n")
    md.append("```bash\nclaude schedule list\n```\n")
    md.append("\n")

    # 6. Como Usar
    md.append("## 🚀 Como Usar Este Índice\n")
    md.append("""
1. **Atualizar Index:**
   ```bash
   python3 /Users/thiago.dias/Claude_CLI/scripts/generate-index.py
   ```

2. **Ver Index:**
   ```bash
   cat /Users/thiago.dias/Claude_CLI/INDEX.md
   ```

3. **Auto-atualizar (rotina):**
   - Configurado em CronCreate cada 7 dias

4. **Buscar algo:**
   - Use Cmd+F no arquivo INDEX.md
   - Procure por nome do skill, MCP, script, etc
""")

    # 7. Resumo Rápido
    md.append("\n## 📊 Resumo Rápido\n")
    md.append(f"- **MCP Servers:** {len(mcp_servers)} ativo(s)\n")
    md.append(f"- **Scripts:** {len(structure['scripts'])} arquivo(s)\n")
    md.append(f"- **Projetos:** {len(structure['analises'])} projeto(s)\n")
    md.append(f"- **Memória:** {len(structure['memoria'])} arquivo(s)\n")
    md.append(f"- **Skills:** {len(skills)} skill(s)\n")

    return "\n".join(md)

def save_index(content):
    """Salva índice em arquivo"""
    index_file = CLAUDE_CLI / "INDEX.md"

    with open(index_file, "w") as f:
        f.write(content)

    print(f"✅ Índice salvo em: {index_file}")
    return index_file

def main():
    """Função principal"""
    print("🔍 Gerando índice do Claude CLI...")
    print()

    content = generate_markdown_index()
    index_file = save_index(content)

    print()
    print("=" * 50)
    print("✅ ÍNDICE GERADO COM SUCESSO!")
    print("=" * 50)
    print()
    print(f"📁 Arquivo: {index_file}")
    print()
    print("📋 Conteúdo do índice:")
    print(content[:500] + "...\n")

if __name__ == "__main__":
    main()
