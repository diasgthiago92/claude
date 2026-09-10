#!/usr/bin/env python3
"""
Integração com BrasilAPI - Exemplo Prático
"""

import requests
import json
import urllib3
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BuscadorBrasilAPI:
    """
    Cliente para BrasilAPI com cache e tratamento de erros.
    """

    def __init__(self, cache_ttl: int = 3600):
        """
        Inicializa o buscador.

        Args:
            cache_ttl: Tempo de vida do cache em segundos (padrão: 1 hora)
        """
        self.base_url = "https://brasilapi.com.br/api/cnpj/v1"
        self.cache = {}
        self.cache_ttl = cache_ttl
        self.timeout = 5

    def buscar(self, cnpj: str) -> Optional[Dict]:
        """
        Busca informações de um CNPJ.

        Args:
            cnpj: CNPJ sem formatação (14 dígitos)

        Returns:
            Dicionário com dados da empresa ou None se não encontrado
        """
        # Remover formatação
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")

        # Verificar cache
        if self._usar_cache(cnpj_limpo):
            print(f"[CACHE] {cnpj_limpo}")
            return self.cache[cnpj_limpo]["dados"]

        # Fazer requisição
        try:
            print(f"[API] Buscando {cnpj_limpo}...")
            url = f"{self.base_url}/{cnpj_limpo}"
            response = requests.get(url, timeout=self.timeout, verify=False)
            response.raise_for_status()

            dados = response.json()

            # Guardar em cache
            self.cache[cnpj_limpo] = {
                "dados": dados,
                "timestamp": datetime.now(),
            }

            return dados

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"[ERRO] CNPJ {cnpj_limpo} não encontrado")
            else:
                print(f"[ERRO] HTTP {response.status_code}: {e}")

            cache_file = Path("cache") / f"{cnpj_limpo}.json"
            if cache_file.exists():
                print(f"[FALLBACK] Usando cache local em {cache_file}")
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None

        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Falha na conexão: {e}")

            cache_file = Path("cache") / f"{cnpj_limpo}.json"
            if cache_file.exists():
                print(f"[FALLBACK] Usando cache local em {cache_file}")
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None

    def _usar_cache(self, cnpj: str) -> bool:
        """Verifica se há cache válido para o CNPJ."""
        if cnpj not in self.cache:
            return False

        cache_entry = self.cache[cnpj]
        idade = (datetime.now() - cache_entry["timestamp"]).total_seconds()

        if idade > self.cache_ttl:
            del self.cache[cnpj]
            return False

        return True

    def buscar_multiplos(self, cnpjs: List[str]) -> Dict[str, Dict]:
        """
        Busca múltiplos CNPJs.

        Args:
            cnpjs: Lista de CNPJs

        Returns:
            Dicionário {cnpj: dados}
        """
        resultados = {}

        for i, cnpj in enumerate(cnpjs, 1):
            print(f"[{i}/{len(cnpjs)}]", end=" ")
            resultado = self.buscar(cnpj)
            resultados[cnpj] = resultado

        return resultados

    def exportar_json(self, dados: Dict, arquivo: str) -> None:
        """Exporta dados para JSON."""
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        print(f"✅ Exportado para: {arquivo}")

    def exportar_csv(self, dados: Dict, arquivo: str) -> None:
        """Exporta dados para CSV."""
        import csv

        if not dados:
            print("Sem dados para exportar")
            return

        # Pegar primeira entrada com dados
        primeira_entrada = next(
            (v for v in dados.values() if v is not None), None
        )

        if not primeira_entrada:
            print("Nenhum resultado com dados")
            return

        # Colunas
        colunas = list(primeira_entrada.keys())

        # Escrever CSV
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()

            for cnpj, dados_cnpj in dados.items():
                if dados_cnpj:
                    writer.writerow(dados_cnpj)
                else:
                    writer.writerow({"cnpj": cnpj, "status": "não encontrado"})

        print(f"✅ Exportado para: {arquivo}")


# Exemplos de uso
if __name__ == "__main__":
    print("=" * 60)
    print("BrasilAPI - Exemplos de Uso")
    print("=" * 60)
    print()

    # Criar cliente
    api = BuscadorBrasilAPI()

    # Exemplo 1: Buscar um CNPJ
    print("📌 Exemplo 1: Buscar um CNPJ")
    print("-" * 60)
    cnpj = "15436940000172"  # Amazon
    dados = api.buscar(cnpj)

    if dados:
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    print()

    # Exemplo 2: Buscar múltiplos CNPJs
    print("📌 Exemplo 2: Buscar múltiplos CNPJs")
    print("-" * 60)
    cnpjs = [
        "15436940000172",  # Amazon
        "15633122000156",  # AWS
        "11222333000181",  # Fake
    ]

    resultados = api.buscar_multiplos(cnpjs)

    print()
    print("Resultados:")
    for cnpj, dados in resultados.items():
        if dados:
            print(f"  {cnpj}: {dados.get('razao_social', 'N/A')}")
        else:
            print(f"  {cnpj}: ❌ Não encontrado")
    print()

    # Exemplo 3: Exportar
    print("📌 Exemplo 3: Exportar para arquivo")
    print("-" * 60)
    api.exportar_json(resultados, "resultados.json")
    api.exportar_csv(resultados, "resultados.csv")
    print()

    # Exemplo 4: Testar cache
    print("📌 Exemplo 4: Testar cache")
    print("-" * 60)
    print("Primeira requisição:")
    api.buscar("15436940000172")
    print("\nSegunda requisição (deve vir do cache):")
    api.buscar("15436940000172")
    print()

    # Mostrar informações do cache
    print("📌 Cache ativo:")
    print(f"Total: {len(api.cache)} itens")
    for cnpj in api.cache:
        print(f"  - {cnpj}")
