#!/usr/bin/env python3
"""
Token Usage Tracker - Rastreador de Tokens Diários
Monitora e gera relatórios de uso de tokens
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

HOME = Path.home()
CLAUDE_CLI = HOME / "Claude_CLI"
TOKEN_LOG_DIR = CLAUDE_CLI / "logs" / "token-usage"
TOKEN_LOG_DIR.mkdir(parents=True, exist_ok=True)

class TokenTracker:
    def __init__(self):
        self.log_dir = TOKEN_LOG_DIR
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_file = self.log_dir / f"tokens-{self.today}.json"

    def get_rtk_stats(self):
        """Obter estatísticas do RTK"""
        try:
            result = subprocess.run(
                ["rtk", "gain"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                output = result.stdout
                # Parse output do RTK
                lines = output.split("\n")
                stats = {}

                for line in lines:
                    if "saved" in line.lower() or "%" in line:
                        stats["rtk_output"] = line.strip()

                return stats
        except Exception as e:
            print(f"⚠️  Erro ao obter RTK stats: {e}")
            return {}

    def get_token_info(self):
        """Coletar informações de tokens do Claude"""
        try:
            # Tentar obter info do Claude
            result = subprocess.run(
                ["claude", "info"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return {
                    "claude_info": result.stdout[:500],  # Primeiros 500 chars
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"⚠️  Erro ao obter info: {e}")

        return {"timestamp": datetime.now().isoformat()}

    def estimate_tokens(self):
        """Estimar tokens usados no dia"""
        # Baseado em RTK, histórico, etc

        rtk_stats = self.get_rtk_stats()

        # Estimar baseado em economia RTK (60-90%)
        # Baseline: ~4k tokens por interação
        base_tokens = 4000

        # Se RTK está ativo, economia é ~75%
        savings_percent = 75
        actual_tokens = base_tokens * (1 - savings_percent/100)

        return {
            "estimated_tokens": actual_tokens,
            "base_tokens": base_tokens,
            "savings_percent": savings_percent,
            "rtk_active": True,
            "rtk_stats": rtk_stats
        }

    def log_token_usage(self, tokens, description="", category="general"):
        """Registrar uso de tokens"""

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tokens": tokens,
            "description": description,
            "category": category,  # general, analysis, coding, mcp, etc
            "token_info": self.get_token_info()
        }

        # Carregar dados existentes
        if self.today_file.exists():
            with open(self.today_file) as f:
                data = json.load(f)
        else:
            data = {
                "date": self.today,
                "entries": [],
                "summary": {}
            }

        data["entries"].append(entry)

        # Atualizar summary
        data["summary"]["total_tokens"] = sum(e["tokens"] for e in data["entries"])
        data["summary"]["num_interactions"] = len(data["entries"])
        data["summary"]["avg_tokens"] = data["summary"]["total_tokens"] / data["summary"]["num_interactions"]
        data["summary"]["last_update"] = datetime.now().isoformat()

        # Salvar
        with open(self.today_file, "w") as f:
            json.dump(data, f, indent=2)

        return entry

    def get_daily_report(self, date=None):
        """Obter relatório do dia"""
        if date is None:
            date = self.today

        log_file = self.log_dir / f"tokens-{date}.json"

        if not log_file.exists():
            return None

        with open(log_file) as f:
            return json.load(f)

    def get_weekly_report(self):
        """Relatório da semana"""
        report = {
            "week_start": (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d"),
            "days": {}
        }

        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily = self.get_daily_report(date)
            if daily:
                report["days"][date] = daily["summary"]

        # Agregado
        total = sum(d.get("total_tokens", 0) for d in report["days"].values())
        report["week_total"] = total
        report["week_avg"] = total / len([d for d in report["days"].values() if "total_tokens" in d])

        return report

    def get_monthly_report(self):
        """Relatório do mês"""
        report = {
            "month": datetime.now().strftime("%Y-%m"),
            "days": {}
        }

        today = datetime.now()
        for i in range(today.day):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            daily = self.get_daily_report(date)
            if daily:
                report["days"][date] = daily["summary"]

        # Agregado
        total = sum(d.get("total_tokens", 0) for d in report["days"].values())
        report["month_total"] = total
        report["month_avg"] = total / len([d for d in report["days"].values() if "total_tokens" in d])

        return report

    def export_csv(self):
        """Exportar para CSV"""
        import csv

        csv_file = self.log_dir / f"tokens-export-{self.today}.csv"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Tokens", "Category", "Description"])

            daily = self.get_daily_report()
            if daily:
                for entry in daily["entries"]:
                    ts = datetime.fromisoformat(entry["timestamp"])
                    writer.writerow([
                        ts.strftime("%Y-%m-%d"),
                        ts.strftime("%H:%M:%S"),
                        entry["tokens"],
                        entry["category"],
                        entry["description"]
                    ])

        return csv_file

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Token Usage Tracker")
    parser.add_argument("command", choices=[
        "log", "daily", "weekly", "monthly", "estimate", "export"
    ])
    parser.add_argument("--tokens", type=int, help="Tokens para logar")
    parser.add_argument("--description", help="Descrição")
    parser.add_argument("--category", default="general", help="Categoria")
    parser.add_argument("--date", help="Data (YYYY-MM-DD)")

    args = parser.parse_args()

    tracker = TokenTracker()

    if args.command == "log":
        if not args.tokens:
            print("❌ --tokens é obrigatório")
            return
        entry = tracker.log_token_usage(
            args.tokens,
            args.description or "",
            args.category
        )
        print(f"✅ Registrado: {entry['tokens']} tokens")

    elif args.command == "daily":
        report = tracker.get_daily_report(args.date)
        if report:
            print(f"\n📊 Relatório Diário - {report['date']}")
            print(f"Total: {report['summary'].get('total_tokens', 0)} tokens")
            print(f"Interações: {report['summary'].get('num_interactions', 0)}")
            print(f"Média: {report['summary'].get('avg_tokens', 0):.0f} tokens/interação")
        else:
            print("❌ Sem dados para este dia")

    elif args.command == "weekly":
        report = tracker.get_weekly_report()
        print(f"\n📊 Relatório Semanal - {report['week_start']}")
        print(f"Total: {report['week_total']} tokens")
        print(f"Média: {report['week_avg']:.0f} tokens/dia")
        print("\nPor dia:")
        for date, data in report["days"].items():
            if "total_tokens" in data:
                print(f"  {date}: {data['total_tokens']} tokens")

    elif args.command == "monthly":
        report = tracker.get_monthly_report()
        print(f"\n📊 Relatório Mensal - {report['month']}")
        print(f"Total: {report['month_total']} tokens")
        print(f"Média: {report['month_avg']:.0f} tokens/dia")

    elif args.command == "estimate":
        estimate = tracker.estimate_tokens()
        print(f"\n📊 Estimativa de Tokens")
        print(f"Base: {estimate['base_tokens']} tokens")
        print(f"Com RTK: {estimate['estimated_tokens']:.0f} tokens")
        print(f"Economia: {estimate['savings_percent']}%")

    elif args.command == "export":
        csv_file = tracker.export_csv()
        print(f"✅ Exportado para: {csv_file}")

if __name__ == "__main__":
    main()
