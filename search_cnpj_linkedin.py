#!/usr/bin/env python3
"""
Script para pesquisar CNPJ + LinkedIn dos sócios
Uso: python3 search_cnpj_linkedin.py <CNPJ>
Exemplo: python3 search_cnpj_linkedin.py 28.015.659/0001-30
"""

import sys
import subprocess
import json
from urllib.parse import quote

def format_cnpj(cnpj):
    """Formata CNPJ com ou sem pontuação"""
    cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")
    return cnpj_clean, f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:14]}"

def search_cnpj_info(cnpj_clean, cnpj_formatted):
    """Busca informações gerais do CNPJ"""
    print(f"\n📋 BUSCANDO INFORMAÇÕES DO CNPJ: {cnpj_formatted}")
    print("=" * 60)

    query = f'"{cnpj_formatted}" OR "{cnpj_clean}" empresa'
    print(f"🔍 Busca: {query}\n")

    # Aqui você integraria com a API de WebSearch
    # Por enquanto, retorna instruções
    return query

def search_socios_linkedin(company_name, socios_names=None):
    """Busca sócios no LinkedIn"""
    print(f"\n👥 BUSCANDO SÓCIOS NO LINKEDIN")
    print("=" * 60)

    if not socios_names:
        # Busca genérica
        queries = [
            f'"{company_name}" sócios site:linkedin.com',
            f'"{company_name}" administrador site:linkedin.com',
            f'"{company_name}" diretores site:linkedin.com'
        ]
    else:
        # Busca específica por sócio
        queries = []
        for name in socios_names:
            queries.append(f'"{name}" site:linkedin.com')

    print("🔗 Queries de busca geradas:")
    for q in queries:
        print(f"  • {q}")

    return queries

def generate_rtk_commands(cnpj_formatted):
    """Gera comandos RTK otimizados"""
    print(f"\n⚡ COMANDOS RTK OTIMIZADOS")
    print("=" * 60)

    commands = [
        f"rtk web search 'CNPJ {cnpj_formatted} empresa'",
        f"rtk web search '{cnpj_formatted} sócios linkedin'",
        f"rtk web fetch 'https://casadosdados.com.br/solucao/cnpj/{cnpj_formatted}'",
    ]

    for cmd in commands:
        print(f"  {cmd}")

    return commands

def main():
    if len(sys.argv) < 2:
        print("❌ Erro: CNPJ não fornecido")
        print("Uso: python3 search_cnpj_linkedin.py <CNPJ>")
        print("Exemplo: python3 search_cnpj_linkedin.py 28.015.659/0001-30")
        sys.exit(1)

    cnpj = sys.argv[1]
    cnpj_clean, cnpj_formatted = format_cnpj(cnpj)

    # Se houver sócios como argumentos adicionais
    socios = sys.argv[2:] if len(sys.argv) > 2 else None

    print("\n" + "="*60)
    print("🔎 PESQUISADOR DE CNPJ + LINKEDIN")
    print("="*60)

    # 1. Busca de informações gerais do CNPJ
    search_cnpj_info(cnpj_clean, cnpj_formatted)

    # 2. Busca de sócios no LinkedIn
    queries = search_socios_linkedin("Luiz Mattos e Engenheiros Associados", socios)

    # 3. Gera comandos RTK
    generate_rtk_commands(cnpj_formatted)

    print("\n" + "="*60)
    print("✅ Scripts gerados! Execute os comandos acima ou use:")
    print(f"   rtk gain  # para ver economia de tokens")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
