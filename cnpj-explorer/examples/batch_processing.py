#!/usr/bin/env python3
"""
Processamento em Batch - Exemplo Avançado
"""

import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import requests


class ProcessadorBatch:
    """
    Processador de lotes de CNPJs com paralelização.
    """

    def __init__(self, max_workers: int = 4, timeout: int = 5):
        """
        Args:
            max_workers: Número de threads para paralelização
            timeout: Timeout para requisições
        """
        self.base_url = "https://brasilapi.com.br/api/cnpj/v1"
        self.max_workers = max_workers
        self.timeout = timeout
        self.resultados = []
        self.erros = []

    def processar_csv(
        self, arquivo_entrada: str, arquivo_saida: str, paralelo: bool = True
    ) -> None:
        """
        Processa arquivo CSV com CNPJs.

        Args:
            arquivo_entrada: Arquivo CSV com coluna 'cnpj'
            arquivo_saida: Arquivo JSON de saída
            paralelo: Usar processamento paralelo
        """
        print(f"📂 Lendo {arquivo_entrada}...")

        cnpjs = []
        with open(arquivo_entrada, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cnpj = row.get("cnpj", "").strip()
                if cnpj:
                    cnpjs.append(cnpj)

        print(f"✅ {len(cnpjs)} CNPJs carregados")
        print()

        # Processar
        if paralelo:
            self._processar_paralelo(cnpjs)
        else:
            self._processar_sequencial(cnpjs)

        # Exportar
        self._exportar_resultados(arquivo_saida)

    def _processar_sequencial(self, cnpjs: List[str]) -> None:
        """Processa CNPJs sequencialmente."""
        print("⏳ Processamento sequencial...")
        tempo_inicio = time.time()

        for i, cnpj in enumerate(cnpjs, 1):
            print(f"[{i}/{len(cnpjs)}] {cnpj}...", end=" ")
            resultado = self._buscar_cnpj(cnpj)
            print(
                "✅" if resultado else "❌"
            )

        tempo_total = time.time() - tempo_inicio
        print(f"\n⏱️  Tempo total: {tempo_total:.2f}s")

    def _processar_paralelo(self, cnpjs: List[str]) -> None:
        """Processa CNPJs em paralelo."""
        print(f"⚡ Processamento paralelo ({self.max_workers} workers)...")
        tempo_inicio = time.time()

        processados = 0
        total = len(cnpjs)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submeter todas as tarefas
            futures = {
                executor.submit(self._buscar_cnpj, cnpj): cnpj for cnpj in cnpjs
            }

            # Processar conforme ficam prontas
            for future in as_completed(futures):
                cnpj = futures[future]
                try:
                    resultado = future.result()
                    processados += 1
                    status = "✅" if resultado else "❌"
                except Exception as e:
                    status = f"⚠️  ({e})"
                    self.erros.append((cnpj, str(e)))

                progresso = (processados / total) * 100
                print(f"[{processados}/{total}] {cnpj}... {status} ({progresso:.1f}%)")

        tempo_total = time.time() - tempo_inicio
        print(f"\n⏱️  Tempo total: {tempo_total:.2f}s")
        print(f"📊 Taxa: {len(cnpjs) / tempo_total:.1f} CNPJs/s")

    def _buscar_cnpj(self, cnpj: str) -> bool:
        """Busca um CNPJ na API."""
        try:
            cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
            url = f"{self.base_url}/{cnpj_limpo}"

            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                dados = response.json()
                self.resultados.append(
                    {
                        "cnpj": cnpj_limpo,
                        "razao_social": dados.get("razao_social"),
                        "municipio": dados.get("municipio"),
                        "status": "encontrado",
                    }
                )
                return True
            else:
                self.resultados.append(
                    {
                        "cnpj": cnpj_limpo,
                        "status": f"erro_http_{response.status_code}",
                    }
                )
                return False

        except Exception as e:
            self.erros.append((cnpj, str(e)))
            self.resultados.append({"cnpj": cnpj, "status": f"erro: {str(e)}"})
            return False

    def _exportar_resultados(self, arquivo: str) -> None:
        """Exporta resultados para JSON."""
        dados_export = {
            "resumo": {
                "total": len(self.resultados),
                "sucesso": sum(1 for r in self.resultados if r.get("status") == "encontrado"),
                "erros": len(self.erros),
            },
            "resultados": self.resultados,
            "erros": self.erros,
        }

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_export, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Resultados exportados para: {arquivo}")
        print(f"   Total: {len(self.resultados)}")
        print(f"   Sucesso: {dados_export['resumo']['sucesso']}")
        print(f"   Erros: {len(self.erros)}")


# Exemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("Processamento em Batch de CNPJs")
    print("=" * 60)
    print()

    # Criar arquivo de teste
    print("📝 Criando arquivo de teste...")
    teste_csv = "teste_cnpjs.csv"

    cnpjs_teste = [
        "15436940000172",  # Amazon
        "15633122000156",  # AWS
        "11222333000181",  # Fake
        "28865114000121",  # Google Brasil
    ]

    with open(teste_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cnpj"])
        writer.writeheader()
        for cnpj in cnpjs_teste:
            writer.writerow({"cnpj": cnpj})

    print(f"✅ Arquivo {teste_csv} criado com {len(cnpjs_teste)} CNPJs")
    print()

    # Processar
    processador = ProcessadorBatch(max_workers=4)

    print("📌 Teste 1: Processamento paralelo")
    print("-" * 60)
    processador.processar_csv(teste_csv, "resultados_paralelo.json", paralelo=True)
    print()

    # Limpar para novo teste
    processador = ProcessadorBatch(max_workers=1)

    print("📌 Teste 2: Processamento sequencial")
    print("-" * 60)
    processador.processar_csv(
        teste_csv, "resultados_sequencial.json", paralelo=False
    )
