#!/usr/bin/env python3
"""
Karajan Monitor - Monitoramento de Economia de Tokens
Rastreia economia diária, semanal e mensal
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class TokenMonitor:
    def __init__(self):
        self.karajan_home = Path(__file__).parent.parent
        self.monitor_file = self.karajan_home / "logs" / "monitor.jsonl"
        self.stats_file = self.karajan_home / "logs" / "stats.json"
        self.history_file = self.karajan_home / "logs" / "history.jsonl"

        # Configuração de tokens por modelo
        self.token_weights = {
            "cheap": 1,      # Haiku
            "balanced": 5,   # Sonnet
            "powerful": 10   # Opus
        }

        self.model_names = {
            "cheap": "Haiku 4.5",
            "balanced": "Sonnet 5",
            "powerful": "Opus 5"
        }

    def log_execution(self, prompt: str, level: str, execution_time: float = 0, tokens_used: int = None):
        """Registra execução de tarefa"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "prompt_preview": prompt[:80].replace("\n", " "),
            "level": level,
            "model": self.model_names.get(level, level),
            "execution_time": execution_time,
            "token_weight": self.token_weights.get(level, 1),
            "tokens_estimated": tokens_used or len(prompt.split()) // 4
        }

        # Criar arquivo se não existir
        self.monitor_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.monitor_file, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def get_daily_report(self, date: str = None) -> dict:
        """Gera relatório diário de economia"""
        if date is None:
            date = datetime.now().date().isoformat()

        if not self.monitor_file.exists():
            return {"date": date, "tasks": 0, "message": "Nenhum dado registrado"}

        daily_tasks = []
        with open(self.monitor_file) as f:
            for line in f:
                entry = json.loads(line)
                if entry["date"] == date:
                    daily_tasks.append(entry)

        if not daily_tasks:
            return {"date": date, "tasks": 0, "message": "Nenhuma tarefa neste dia"}

        # Calcular economia
        baseline = len(daily_tasks) * self.token_weights["powerful"]
        actual = sum(task["token_weight"] for task in daily_tasks)
        savings = ((baseline - actual) / baseline * 100) if baseline > 0 else 0

        # Distribuição por nível
        distribution = defaultdict(int)
        for task in daily_tasks:
            distribution[task["level"]] += 1

        return {
            "date": date,
            "tasks": len(daily_tasks),
            "distribution": dict(distribution),
            "baseline_tokens": baseline,
            "actual_tokens": actual,
            "tokens_saved": baseline - actual,
            "savings_percent": round(savings, 1),
            "average_execution_time": sum(t.get("execution_time", 0) for t in daily_tasks) / len(daily_tasks)
        }

    def get_weekly_report(self, weeks_back: int = 0) -> dict:
        """Gera relatório semanal"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday() + (weeks_back * 7))
        week_end = week_start + timedelta(days=6)

        if not self.monitor_file.exists():
            return {"week": f"{week_start} a {week_end}", "tasks": 0}

        weekly_tasks = []
        with open(self.monitor_file) as f:
            for line in f:
                entry = json.loads(line)
                task_date = datetime.fromisoformat(entry["date"]).date()
                if week_start <= task_date <= week_end:
                    weekly_tasks.append(entry)

        if not weekly_tasks:
            return {"week": f"{week_start} a {week_end}", "tasks": 0}

        baseline = len(weekly_tasks) * self.token_weights["powerful"]
        actual = sum(task["token_weight"] for task in weekly_tasks)
        savings = ((baseline - actual) / baseline * 100) if baseline > 0 else 0

        distribution = defaultdict(int)
        for task in weekly_tasks:
            distribution[task["level"]] += 1

        return {
            "week": f"{week_start} a {week_end}",
            "tasks": len(weekly_tasks),
            "distribution": dict(distribution),
            "baseline_tokens": baseline,
            "actual_tokens": actual,
            "tokens_saved": baseline - actual,
            "savings_percent": round(savings, 1)
        }

    def get_monthly_report(self, months_back: int = 0) -> dict:
        """Gera relatório mensal completo"""
        today = datetime.now().date()
        month_start = (today.replace(day=1) - timedelta(days=months_back * 30)).replace(day=1)

        # Próximo mês começa no dia 1
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)

        if not self.monitor_file.exists():
            return {"month": month_start.strftime("%Y-%m"), "tasks": 0}

        monthly_tasks = []
        with open(self.monitor_file) as f:
            for line in f:
                entry = json.loads(line)
                task_date = datetime.fromisoformat(entry["date"]).date()
                if month_start <= task_date <= month_end:
                    monthly_tasks.append(entry)

        if not monthly_tasks:
            return {
                "month": month_start.strftime("%Y-%m"),
                "tasks": 0,
                "message": "Nenhuma tarefa neste mês"
            }

        # Cálculos detalhados
        baseline = len(monthly_tasks) * self.token_weights["powerful"]
        actual = sum(task["token_weight"] for task in monthly_tasks)
        savings = baseline - actual
        savings_percent = ((baseline - actual) / baseline * 100) if baseline > 0 else 0

        # Distribuição
        distribution = defaultdict(int)
        models_used = defaultdict(int)
        for task in monthly_tasks:
            distribution[task["level"]] += 1
            models_used[task["model"]] += 1

        # Análise por tipo
        prompt_lengths = defaultdict(list)
        execution_times = []
        for task in monthly_tasks:
            prompt_lengths[task["level"]].append(task["tokens_estimated"])
            execution_times.append(task.get("execution_time", 0))

        return {
            "month": month_start.strftime("%Y-%m"),
            "period": f"{month_start} a {month_end}",
            "total_tasks": len(monthly_tasks),
            "distribution_by_level": dict(distribution),
            "models_used": dict(models_used),
            "baseline_tokens": baseline,
            "actual_tokens": actual,
            "tokens_saved": savings,
            "savings_percent": round(savings_percent, 1),
            "savings_message": f"🎵 Karajan economizou {savings:,.0f} tokens ({savings_percent:.0f}%) em {len(monthly_tasks)} tarefas!",
            "average_execution_time": round(sum(execution_times) / len(execution_times), 2) if execution_times else 0,
            "tasks_per_day": round(len(monthly_tasks) / (month_end - month_start).days, 1),
            "breakdown": {
                "cheap_tokens_saved": (distribution.get("cheap", 0) * self.token_weights["powerful"]) - (distribution.get("cheap", 0) * self.token_weights["cheap"]),
                "balanced_tokens_saved": (distribution.get("balanced", 0) * self.token_weights["powerful"]) - (distribution.get("balanced", 0) * self.token_weights["balanced"]),
                "powerful_tokens_saved": 0  # Opus não economiza tokens
            }
        }

    def get_all_time_stats(self) -> dict:
        """Gera estatísticas desde o início do uso"""
        if not self.monitor_file.exists():
            return {"message": "Nenhum dado registrado"}

        all_tasks = []
        with open(self.monitor_file) as f:
            for line in f:
                all_tasks.append(json.loads(line))

        if not all_tasks:
            return {"message": "Nenhum dado registrado"}

        baseline = len(all_tasks) * self.token_weights["powerful"]
        actual = sum(task["token_weight"] for task in all_tasks)
        savings = baseline - actual
        savings_percent = ((baseline - actual) / baseline * 100) if baseline > 0 else 0

        distribution = defaultdict(int)
        for task in all_tasks:
            distribution[task["level"]] += 1

        first_task = all_tasks[0]
        last_task = all_tasks[-1]
        days_active = (datetime.fromisoformat(last_task["timestamp"]).date() -
                      datetime.fromisoformat(first_task["timestamp"]).date()).days + 1

        return {
            "total_tasks": len(all_tasks),
            "days_active": days_active,
            "first_task": first_task["timestamp"],
            "last_task": last_task["timestamp"],
            "distribution": dict(distribution),
            "baseline_tokens": baseline,
            "actual_tokens": actual,
            "tokens_saved": savings,
            "savings_percent": round(savings_percent, 1),
            "average_tokens_per_task": round(actual / len(all_tasks), 1),
            "average_tasks_per_day": round(len(all_tasks) / days_active, 1) if days_active > 0 else 0
        }


def print_monthly_report(report: dict):
    """Formata relatório mensal para exibição"""
    print(f"\n📊 RELATÓRIO MENSAL - {report['month']}")
    print("=" * 70)

    print(f"\n📈 Resumo:")
    print(f"  Total de tarefas: {report['total_tasks']}")
    print(f"  Período: {report['period']}")
    print(f"  Tarefas por dia: {report['tasks_per_day']}")
    print(f"  Tempo médio: {report['average_execution_time']}s")

    print(f"\n💰 Economia de Tokens:")
    print(f"  Baseline (sempre Opus): {report['baseline_tokens']:,} tokens")
    print(f"  Tokens gastos (com Karajan): {report['actual_tokens']:,} tokens")
    print(f"  Tokens economizados: {report['tokens_saved']:,} ✅")
    print(f"  Economia: {report['savings_percent']:.1f}% 🎵")
    print(f"\n  {report['savings_message']}")

    print(f"\n📊 Distribuição por Modelo:")
    for level, count in report['distribution_by_level'].items():
        print(f"  {report['models_used'].get(level, level)}: {count} tarefas")

    print(f"\n🔍 Economia por Tipo:")
    print(f"  Tarefas Cheap (Haiku): {report['breakdown']['cheap_tokens_saved']:,} tokens economizados")
    print(f"  Tarefas Balanced (Sonnet): {report['breakdown']['balanced_tokens_saved']:,} tokens economizados")
    print(f"  Tarefas Powerful (Opus): 0 tokens (melhor modelo)")

    print("=" * 70 + "\n")


def main():
    import sys

    monitor = TokenMonitor()

    if len(sys.argv) < 2:
        # Mostrar relatório mensal atual
        report = monitor.get_monthly_report()
        print_monthly_report(report)
        return

    command = sys.argv[1]

    if command == "today":
        report = monitor.get_daily_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif command == "weekly":
        weeks_back = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        report = monitor.get_weekly_report(weeks_back)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif command == "monthly":
        months_back = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        report = monitor.get_monthly_report(months_back)
        print_monthly_report(report)

    elif command == "all-time":
        stats = monitor.get_all_time_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif command == "log":
        if len(sys.argv) < 3:
            print("Uso: monitor.py log <prompt> <level> [execution_time] [tokens_used]")
            sys.exit(1)
        prompt = sys.argv[2]
        level = sys.argv[3]
        execution_time = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        tokens_used = int(sys.argv[5]) if len(sys.argv) > 5 else None
        entry = monitor.log_execution(prompt, level, execution_time, tokens_used)
        print(json.dumps(entry, ensure_ascii=False))

    else:
        print("Uso: monitor.py [today|weekly|monthly|all-time|log]")
        sys.exit(1)


if __name__ == "__main__":
    main()
