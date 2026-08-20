#!/usr/bin/env python3
"""
Karajan Phase 1 - Wrapper Completo
Classifica tarefa → Executa com modelo certo → Registra economia
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
from orchestrator import Karajan


class KarajanPhase1:
    def __init__(self):
        self.karajan = Karajan()
        self.config_path = Path(__file__).parent.parent / "config" / "economy.json"
        self.economy_config = self._load_economy_config()

    def _load_economy_config(self):
        """Carrega política de economia de tokens"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return self._default_economy_config()

    def _default_economy_config(self):
        """Configuração padrão de economia"""
        return {
            "enabled": True,
            "strategies": {
                "cheap": {
                    "compression": "aggressive",
                    "context_limit": 2000,
                    "summarize_old_context": True,
                    "use_prompt_caching": True,
                    "remove_comments": True,
                    "remove_whitespace": True,
                    "truncate_long_outputs": True
                },
                "balanced": {
                    "compression": "moderate",
                    "context_limit": 10000,
                    "summarize_old_context": True,
                    "use_prompt_caching": True,
                    "remove_comments": False,
                    "remove_whitespace": True,
                    "truncate_long_outputs": False
                },
                "powerful": {
                    "compression": "minimal",
                    "context_limit": 100000,
                    "summarize_old_context": False,
                    "use_prompt_caching": True,
                    "remove_comments": False,
                    "remove_whitespace": False,
                    "truncate_long_outputs": False
                }
            },
            "techniques": {
                "prompt_caching": {
                    "enabled": True,
                    "description": "Reutiliza tokens de prompts frequentes (cache nativo Claude)"
                },
                "context_compression": {
                    "enabled": True,
                    "description": "Remove comentários, whitespace, código não-essencial"
                },
                "context_summarization": {
                    "enabled": True,
                    "description": "Resume contexto antigo em 1-2 linhas antes de nova tarefa"
                },
                "selective_context": {
                    "enabled": True,
                    "description": "Inclui apenas arquivos/funções relevantes, não toda repo"
                },
                "rtk_integration": {
                    "enabled": True,
                    "description": "Usa RTK para compressão adicional de comandos e histórico git"
                }
            }
        }

    def compress_context(self, context: str, level: str) -> str:
        """Comprime contexto baseado no nível de modelo"""
        config = self.economy_config["strategies"].get(level, {})

        compressed = context

        # Remove comentários se configurado
        if config.get("remove_comments"):
            import re
            # Remove comentários de linha única
            compressed = re.sub(r'//.*?$', '', compressed, flags=re.MULTILINE)
            # Remove comentários de bloco
            compressed = re.sub(r'/\*.*?\*/', '', compressed, flags=re.DOTALL)
            # Remove comentários Python
            compressed = re.sub(r'#.*?$', '', compressed, flags=re.MULTILINE)

        # Remove whitespace excessivo se configurado
        if config.get("remove_whitespace"):
            compressed = re.sub(r'\n\n+', '\n', compressed)  # Remove linhas em branco múltiplas
            compressed = re.sub(r'  +', ' ', compressed)  # Remove espaços múltiplos

        # Truncar se necessário
        max_chars = config.get("context_limit", 100000) * 4  # ~4 chars por token
        if len(compressed) > max_chars:
            compressed = compressed[:max_chars] + f"\n... [contexto truncado, {len(compressed) - max_chars} caracteres removidos]"

        return compressed

    def prepare_prompt_for_claude(self, user_prompt: str, context: str = None, level: str = "balanced") -> str:
        """Prepara prompt otimizado para economia de tokens"""
        config = self.economy_config["strategies"].get(level, {})

        # Construir prompt otimizado
        parts = []

        # Adicionar contexto comprimido se disponível
        if context:
            compressed_context = self.compress_context(context, level)
            parts.append(f"## Contexto\n{compressed_context}\n")

        # Adicionar prompt do usuário
        parts.append(f"## Tarefa\n{user_prompt}")

        # Adicionar instrução de economia se cheap
        if level == "cheap":
            parts.append("\n\n**⚡ Nota**: Responda de forma concisa e direta (este é um modelo otimizado para velocidade).")

        return "\n".join(parts)

    def call_claude_api(self, prompt: str, model: str) -> str:
        """Chama Claude API via CLI do Claude Code"""
        try:
            # Usar o claude command com modelo específico
            result = subprocess.run(
                ["claude", "--model", model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Claude Error: {result.stderr}")
        except Exception as e:
            return f"❌ Erro ao chamar Claude: {str(e)}"

    def execute_task(self, user_prompt: str, context: str = None, force_level: str = None) -> dict:
        """
        Executa a tarefa completa: classifica → otimiza → executa → registra
        """
        execution_start = datetime.now()

        # Classificar
        task_decision = self.karajan.get_model(user_prompt, {"files": 1, "lines": len(user_prompt.split('\n'))})
        level = force_level or task_decision["level"]
        model = task_decision["model"]

        # Preparar prompt otimizado
        optimized_prompt = self.prepare_prompt_for_claude(user_prompt, context, level)

        # Executar
        response = self.call_claude_api(optimized_prompt, model)

        # Registrar
        execution_time = (datetime.now() - execution_start).total_seconds()
        self.karajan.log_decision(user_prompt, task_decision)

        return {
            "success": True,
            "level": level,
            "model": model,
            "response": response,
            "execution_time": execution_time,
            "optimization_level": self.economy_config["strategies"][level]["compression"],
            "tokens_estimate": len(optimized_prompt.split()) // 4,  # Aproximado: ~4 chars por token
        }

    def batch_execute(self, tasks: list) -> list:
        """Executa múltiplas tarefas com reutilização de contexto e cache"""
        results = []

        for i, task in enumerate(tasks):
            # Para tarefas batch, usar contexto agregado das tarefas anteriores
            previous_context = "\n---\n".join([t.get("response", "")[:100] for t in results if "response" in t])

            result = self.execute_task(
                task.get("prompt", ""),
                context=previous_context if i > 0 else None
            )
            results.append(result)

        return results

    def get_economy_report(self) -> dict:
        """Gera relatório detalhado de economia"""
        stats_file = Path(__file__).parent.parent / "logs" / "stats.json"
        history_file = Path(__file__).parent.parent / "logs" / "history.jsonl"

        stats = {}
        if stats_file.exists():
            with open(stats_file) as f:
                stats = json.load(f)

        weights = self.economy_config.get("models", {})
        if not weights:
            weights = self.karajan.config["token_weights"]

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": sum(stats.values()),
            "distribution": stats,
            "economy_strategies_enabled": [
                name for name, conf in self.economy_config["techniques"].items()
                if conf.get("enabled")
            ],
            "estimated_savings": self._calculate_savings(stats, weights)
        }

        return report

    def _calculate_savings(self, stats: dict, weights: dict) -> dict:
        """Calcula economia estimada com e sem compressão"""
        total_tasks = sum(stats.values())

        # Baseline: sempre usar Opus
        baseline_tokens = total_tasks * weights.get("powerful", 10)

        # Atual: com Karajan routing
        actual_tokens = sum(
            stats.get(level, 0) * weights.get(level, 1)
            for level in ["cheap", "balanced", "powerful"]
        )

        # Com compressão: reduz tokens em ~30-50% por tarefa
        compression_reduction = 0.35  # Média 35%
        compressed_tokens = actual_tokens * (1 - compression_reduction)

        return {
            "baseline_all_opus": baseline_tokens,
            "with_karajan_routing": actual_tokens,
            "with_compression": compressed_tokens,
            "savings_routing_percent": ((baseline_tokens - actual_tokens) / baseline_tokens * 100) if baseline_tokens else 0,
            "savings_compression_percent": ((actual_tokens - compressed_tokens) / actual_tokens * 100) if actual_tokens else 0,
            "total_savings_percent": ((baseline_tokens - compressed_tokens) / baseline_tokens * 100) if baseline_tokens else 0,
        }


def main():
    if len(sys.argv) < 2:
        print("Uso: python phase1_wrapper.py <prompt> [--context <arquivo>] [--force-level cheap/balanced/powerful]")
        sys.exit(1)

    prompt = sys.argv[1]
    context = None
    force_level = None

    # Parsear argumentos
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--context" and i + 2 < len(sys.argv):
            context_file = sys.argv[i + 3]
            if Path(context_file).exists():
                with open(context_file) as f:
                    context = f.read()
        elif arg == "--force-level" and i + 2 < len(sys.argv):
            force_level = sys.argv[i + 3]
        elif arg == "--report":
            phase1 = KarajanPhase1()
            report = phase1.get_economy_report()
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return

    phase1 = KarajanPhase1()
    result = phase1.execute_task(prompt, context, force_level)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
