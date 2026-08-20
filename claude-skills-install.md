# Instalação de Skills e Ferramentas para Claude Code

Arquivo gerado em 2026-08-19 com instruções de instalação dos repositórios selecionados.

---

## 📋 Pré-requisitos

- Claude Code CLI instalado (`npm install -g @anthropic-ai/claude-code`)
- Git instalado
- Node.js 18+

---

## 1. phuryn/pm-skills — Skills de Product Management

**O que faz:** 68 skills de PM e 42 workflows encadeados em 9 plugins. Cobrem descoberta, estratégia, execução, launch, growth e shipping de código com IA.

**Compatível com:** Claude Code, Codex, Cowork e outros agentes.

### Instalação

```bash
# Passo 1: Adicionar o marketplace
claude plugin marketplace add phuryn/pm-skills

# Passo 2: Instalar todos os plugins (ou escolher apenas os que quiser)
claude plugin install pm-toolkit@pm-skills
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-market-research@pm-skills
claude plugin install pm-data-analytics@pm-skills
claude plugin install pm-marketing-growth@pm-skills
claude plugin install pm-go-to-market@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-ai-shipping@pm-skills
```

### Comandos disponíveis após instalação

- `/discover` — brainstorm de ideias e identificação de assumptions
- `/strategy` — clareza estratégica de produto
- `/write-prd` — escrever PRDs estruturados
- `/plan-launch` — planejamento de launch
- `/north-star` — definição de métricas north star

**Repo:** https://github.com/phuryn/pm-skills

---

## 2. JimLiu/baoyu-design — Claude Design como Agent Skill

**O que faz:** Empacota o Claude Design (engine do claude.ai/design) como uma skill portável. Gera mockups de UI, protótipos interativos, wireframes, landing pages, dashboards, apps mobile e slide decks — tudo como HTML autocontido.

**Compatível com:** Cursor, Claude Code, Claude Desktop, Codex e qualquer agente que leia SKILL.md.

**Melhor com:** Claude Opus 4.8 (mas funciona com outros modelos).

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/JimLiu/baoyu-design.git

# Copiar a skill para o diretório de skills do Claude Code
cp -R baoyu-design ~/.claude/skills/baoyu-design

# Ou copiar para um projeto específico
cp -R baoyu-design .claude/skills/baoyu-design
```

### Uso

Após instalado, basta pedir ao Claude para criar designs:
- "Build a Reader Mac app UI"
- "Create a dashboard for analytics"
- "Design a mobile onboarding flow"

Os artefatos são salvos em `designs/<project>/` como HTML autocontido.

**Repo:** https://github.com/JimLiu/baoyu-design

---

## 3. saadeghi/daisyui — Biblioteca de Componentes Tailwind CSS

**O que faz:** Biblioteca de componentes open-source mais popular para Tailwind CSS. Componentes prontos, estilizados e acessíveis para construção rápida de interfaces.

### Instalação (npm)

```bash
# Instalar via npm no seu projeto
npm install daisyui
```

### Configuração no tailwind.config.js

```js
import daisyui from 'daisyui';

export default {
  plugins: [daisyui()],
  // Para escolher temas específicos:
  daisyui: {
    themes: ['light', 'dark', 'cupcake', 'synthwave'], // 35+ temas disponíveis
  },
};
```

### Instalação via CDN (para protótipos rápidos)

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
```

**Site oficial:** https://daisyui.com
**Repo:** https://github.com/saadeghi/daisyui

---

## 4. DouyinFE/semi-design — Design System + Design-to-Code

**O que faz:** Design system moderno e biblioteca React UI com 3000+ design tokens. Feature de Design-to-Code em um clique. AI-friendly.

### Instalação (npm)

```bash
# Instalar Semi UI no seu projeto React
npm install @douyinfe/semi-ui @douyinfe/semi-icons
```

### Uso básico

```jsx
import { Button } from '@douyinfe/semi-ui';

function App() {
  return <Button theme="solid">Hello Semi</Button>;
}
```

### Figma UIKit

Disponível em: https://www.figma.com/@semi

**Repo:** https://github.com/DouyinFE/semi-design

---

## 5. lucide-icons/lucide — Toolkit de Ícones

**O que faz:** Biblioteca open-source com 1600+ ícones vetoriais (SVG). Fork do Feather Icons. Leve, consistente e customizável.

### Instalação (npm)

```bash
# Pacote principal (React)
npm install lucide-react

# Para Vue
npm install lucide-vue-next

# Para Svelte
npm install lucide-svelte

# Para Angular
npm install lucide-angular

# CLI para usar ícones em qualquer projeto
npm install -g lucide-static
```

### Uso (React)

```jsx
import { Camera, Heart, Settings } from 'lucide-react';

function App() {
  return (
    <div>
      <Camera size={24} color="currentColor" />
      <Heart size={24} strokeWidth={2} />
      <Settings size={24} />
    </div>
  );
}
```

### Uso via CDN (HTML direto)

```html
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="camera"></i>
<script>lucide.createIcons();</script>
```

**Site oficial:** https://lucide.dev
**Repo:** https://github.com/lucide-icons/lucide

---

## 6. RefoundAI/lenny-skills — Skills de PM do Lenny's Podcast

**O que faz:** 76 skills de product management e engineering, destilados de 597 episódios do Lenny's Podcast e 349 posts da newsletter. Cada skill inclui frameworks, templates e quotes verificados.

### Instalação

```bash
# Passo 1: Clonar o repositório
git clone https://github.com/RefoundAI/lenny-skills.git

# Passo 2: Copiar skills individuais para .claude/skills/
# Exemplo: instalar skill de writing-prds
cp -R lenny-skills/skills/writing-prds .claude/skills/

# Exemplo: instalar skill de north-star-metrics
cp -R lenny-skills/skills/north-star-metrics .claude/skills/

# Para instalar TODAS as skills de uma vez:
cp -R lenny-skills/skills/* .claude/skills/
```

### Skills disponíveis (categorias)

**Estratégia & Posicionamento:**
- defining-product-strategy, product-vision, positioning, pricing-strategy, north-star-metrics, measuring-pmf, competitive-strategy, recovering-from-failure

**Planejamento & Priorização:**
- roadmap-prioritization, goal-setting-okrs, planning-cadence, high-stakes-decisions

**Discovery & Research:**
- user-research, customer-interviews, assumption-mapping, opportunity-solution-tree

**Building & Execution:**
- writing-prds, product-specs, feature-prioritization, mvp-thinking

**Launch & Growth:**
- go-to-market, product-launch, growth-loops, retention-strategy

**Team & Operating:**
- hiring-pms, team-structure, product-councils, engineering-collaboration

**Repo:** https://github.com/RefoundAI/lenny-skills
**Navegador de skills:** https://refoundai.com/lenny-skills/

---

## 7. linshenkx/prompt-optimizer — Otimizador de Prompts IA

**O que faz:** Ferramenta de otimização de prompts com IA. Ajuda a escrever prompts melhores e obter melhores resultados. Suporta múltiplos modelos (OpenAI, Gemini, DeepSeek, Grok, etc).

**Plataformas:** Web app, Desktop app, Chrome extension, Docker.

### Instalação

#### Opção A: Usar online (sem instalação)
Acesse: https://prompt.always200.com

#### Opção B: Docker (self-hosted)

```bash
docker run -d \
  --name prompt-optimizer \
  -p 80:80 \
  linshenkx/prompt-optimizer:latest
```

#### Opção C: Chrome Extension
Buscar "Prompt Optimizer" na Chrome Web Store.

#### Opção D: Desktop App
Baixar em: https://github.com/linshenkx/prompt-optimizer/releases

### Integração com Claude (MCP)

O Prompt Optimizer suporta o protocolo MCP (Model Context Protocol), permitindo integração direta com Claude Desktop:

1. Abra as configurações do Claude Desktop
2. Adicione o servidor MCP do Prompt Optimizer
3. Use a otimização de prompts diretamente no Claude

**Repo:** https://github.com/linshenkx/prompt-optimizer

---

## 🚀 Script de Instalação Rápida (todos de uma vez)

```bash
#!/bin/bash
# Script para instalar todas as skills e ferramentas

echo "🔧 Instalando PM Skills (phuryn/pm-skills)..."
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-toolkit@pm-skills
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-market-research@pm-skills
claude plugin install pm-data-analytics@pm-skills
claude plugin install pm-marketing-growth@pm-skills
claude plugin install pm-go-to-market@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-ai-shipping@pm-skills

echo "🎨 Instalando baoyu-design..."
git clone https://github.com/JimLiu/baoyu-design.git /tmp/baoyu-design
mkdir -p ~/.claude/skills
cp -R /tmp/baoyu-design ~/.claude/skills/baoyu-design

echo "📚 Instalando lenny-skills..."
git clone https://github.com/RefoundAI/lenny-skills.git /tmp/lenny-skills
cp -R /tmp/lenny-skills/skills/* ~/.claude/skills/

echo "✅ Skills instaladas! Reinicie o Claude Code para ativar."
```

---

## 📁 Estrutura de diretórios do Claude Code

```
~/.claude/
├── skills/                    # Skills globais
│   ├── baoyu-design/
│   ├── writing-prds/
│   ├── north-star-metrics/
│   └── ...
├── plugins/                   # Plugins instalados
└── config.json               # Configuração
```

Para um projeto específico:
```
meu-projeto/
├── .claude/
│   └── skills/               # Skills do projeto
└── ...
```

---

## 📝 Notas

- Skills de PM (phuryn e lenny-skills) se complementam — pode instalar ambas sem conflito
- daisyui e semi-design são bibliotecas de UI (instalar no projeto, não no Claude)
- lucide é biblioteca de ícones (instalar no projeto)
- baoyu-design é uma skill do Claude (instalar em ~/.claude/skills/)
- prompt-optimizer é uma ferramenta standalone (web/desktop/docker)
- Após instalar skills, reinicie o Claude Code para que sejam carregadas
