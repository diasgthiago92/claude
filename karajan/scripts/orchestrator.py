#!/usr/bin/env python3
"""
Karajan - Modelo Orquestrador Inteligente
Roteia tarefas para o modelo certo, economizando tokens
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class Karajan:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "routes.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.logs_dir = Path(__file__).parent.parent / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.stats_file = self.logs_dir / "stats.json"
        self.history_file = self.logs_dir / "history.jsonl"

    def _load_config(self):
        with open(self.config_path) as f:
            return json.load(f)

    def classify_task(self, prompt: str, context_size: dict = None) -> str:
        """
        Classifica a tarefa e retorna o nível de modelo necessário.
        Returns: "cheap", "balanced", ou "powerful"
        """
        prompt_lower = prompt.lower()
        context_size = context_size or {}

        # Verificar palavras-chave de nível powerful
        for keyword in self.config["classification_rules"]["powerful_keywords"]:
            if keyword in prompt_lower:
                return "powerful"

        # Verificar limites de contexto
        files = context_size.get("files", 0)
        lines = context_size.get("lines", 0)

        balanced_max_files = self.config["context_thresholds"]["balanced_max_files"]
        balanced_max_lines = self.config["context_thresholds"]["balanced_max_lines"]
        cheap_max_files = self.config["context_thresholds"]["cheap_max_files"]
        cheap_max_lines = self.config["context_thresholds"]["cheap_max_lines"]

        if files > balanced_max_files or lines > balanced_max_lines:
            return "powerful"

        # Verificar palavras-chave de nível balanced
        for keyword in self.config["classification_rules"]["balanced_keywords"]:
            if keyword in prompt_lower:
                return "balanced"

        if files > cheap_max_files or lines > cheap_max_lines:
            return "balanced"

        # Padrão: cheap (economizador)
        return "cheap"

    def get_model(self, prompt: str, context_size: dict = None) -> dict:
        """
        Obtém a recomendação de modelo para a tarefa.
        Retorna: {"level": str, "model": str, "reason": str}
        """
        level = self.classify_task(prompt, context_size)
        model = self.config["models"][level]

        reasons = {
            "cheap": "Tarefa simples - usando Haiku 4.5 para economia máxima",
            "balanced": "Complexidade média - usando Sonnet 5 para equilíbrio",
            "powerful": "Tarefa complexa - usando Opus 5 para máxima precisão"
        }

        return {
            "level": level,
            "model": model,
            "reason": reasons[level],
            "token_weight": self.config["token_weights"][level]
        }

    def log_decision(self, prompt: str, decision: dict, context_size: dict = None):
        """Registra a decisão de roteamento para análise posterior"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt_preview": prompt[:100].replace("\n", " "),
            "decision": decision,
            "context_size": context_size or {}
        }

        # Adicionar ao histórico
        with open(self.history_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Atualizar estatísticas
        self._update_stats(decision["level"])

    def _update_stats(self, level: str):
        """Atualiza estatísticas de uso"""
        stats = {}
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                stats = json.load(f)

        stats.setdefault(level, 0)
        stats[level] += 1

        with open(self.stats_file, "w") as f:
            json.dump(stats, f, indent=2)

    def get_savings_report(self):
        """Retorna relatório de economia de tokens"""
        if not self.stats_file.exists():
            return {"message": "Nenhum dado de economia ainda"}

        with open(self.stats_file) as f:
            stats = json.load(f)

        total_uses = sum(stats.values())
        weights = self.config["token_weights"]

        # Calcular economia (baseline = always using powerful)
        baseline_cost = total_uses * weights["powerful"]
        actual_cost = sum(stats.get(level, 0) * weights[level] for level in ["cheap", "balanced", "powerful"])
        savings_percent = ((baseline_cost - actual_cost) / baseline_cost * 100) if baseline_cost > 0 else 0

        return {
            "total_tasks": total_uses,
            "distribution": stats,
            "estimated_baseline_cost": baseline_cost,
            "estimated_actual_cost": actual_cost,
            "savings_percent": round(savings_percent, 1),
            "savings_message": f"🎵 Karajan economizou ~{savings_percent:.0f}% de tokens!"
        }


def main():
    if len(sys.argv) < 2:
        print("Uso: python orchestrator.py <prompt> [--context-files N] [--context-lines N]")
        sys.exit(1)

    prompt = sys.argv[1]

    # Parsear contexto se fornecido
    context_size = {}
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--context-files" and i + 2 < len(sys.argv):
            context_size["files"] = int(sys.argv[i + 3])
        elif arg == "--context-lines" and i + 2 < len(sys.argv):
            context_size["lines"] = int(sys.argv[i + 3])

    karajan = Karajan()
    decision = karajan.get_model(prompt, context_size)
    karajan.log_decision(prompt, decision, context_size)

    # Output para ser parseado
    print(json.dumps(decision, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
