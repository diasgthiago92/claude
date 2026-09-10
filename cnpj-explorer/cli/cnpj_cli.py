#!/usr/bin/env python3
"""
CNPJ Explorer CLI - Ferramenta completa para consultar CNPJs brasileiros
"""

import sys
import os
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.validate_cnpj import validar_cnpj, formatar_cnpj
from examples.brasilapi_integration import BuscadorBrasilAPI
from core.relatorio import RelatorioCNPJ


class CNPJCLI:
    """Interface CLI para CNPJ Explorer"""

    def __init__(self):
        self.buscador = BuscadorBrasilAPI()
        self.cache_dir = Path("./cache")
        self.output_dir = Path("./output")
        self.log_file = Path("./logs/cnpj_explorer.log")

        # Criar diretórios se não existirem
        self.cache_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.log_file.parent.mkdir(exist_ok=True)

    def validar(self, cnpj: str) -> bool:
        """Valida um CNPJ"""
        if validar_cnpj(cnpj):
            formatado = formatar_cnpj(cnpj)
            print(f"✅ CNPJ válido")
            print(f"   Formatado: {formatado}")
            return True
        else:
            print(f"❌ CNPJ inválido")
            return False

    def buscar_cnpj(self, cnpj: str, output_format: str = "json") -> None:
        """Busca informações de um CNPJ"""
        # Validar primeiro
        if not validar_cnpj(cnpj):
            print(f"❌ CNPJ inválido: {cnpj}")
            return

        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        print(f"🔍 Buscando CNPJ: {formatar_cnpj(cnpj_limpo)}...")

        dados = self.buscador.buscar(cnpj_limpo)

        if dados:
            self._exibir_dados(dados, output_format)
        else:
            print(f"❌ CNPJ não encontrado ou erro na API")

    def buscar_multiplos(
        self, cnpjs: List[str], output_file: Optional[str] = None
    ) -> None:
        """Busca múltiplos CNPJs"""
        print(f"🔍 Buscando {len(cnpjs)} CNPJs...\n")

        resultados = self.buscador.buscar_multiplos(cnpjs)

        # Exibir resumo
        encontrados = sum(1 for r in resultados.values() if r is not None)
        print(f"\n📊 Resumo: {encontrados}/{len(cnpjs)} encontrados")

        # Exportar se solicitado
        if output_file:
            self._exportar_resultados(resultados, output_file)

    def processar_csv(
        self,
        arquivo_entrada: str,
        arquivo_saida: Optional[str] = None,
        paralelo: bool = False,
        workers: int = 4,
    ) -> None:
        """Processa arquivo CSV"""
        from examples.batch_processing import ProcessadorBatch

        if not arquivo_saida:
            arquivo_saida = f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        processador = ProcessadorBatch(max_workers=workers)
        processador.processar_csv(arquivo_entrada, arquivo_saida, paralelo=paralelo)

    def limpar_cache(self) -> None:
        """Limpa o cache"""
        self.buscador.cache.clear()
        print("✅ Cache limpo")

    def info_cache(self) -> None:
        """Mostra informações do cache"""
        print(f"📊 Cache ativo:")
        print(f"   Total de itens: {len(self.buscador.cache)}")

        if self.buscador.cache:
            print(f"\n   CNPJs em cache:")
            for cnpj in list(self.buscador.cache.keys())[:10]:
                print(f"   - {cnpj}")

            if len(self.buscador.cache) > 10:
                print(f"   ... e mais {len(self.buscador.cache) - 10}")

    def gerar_relatorio_completo(
        self,
        cnpj: str,
        output_format: str = "markdown",
        output_file: Optional[str] = None
    ) -> None:
        """Gera relatório completo: sócios + LinkedIn + situação fiscal + Portal da Transparência"""
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        cnpj_fmt = f"{cnpj_limpo[0:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:14]}" if len(cnpj_limpo) == 14 else cnpj
        print(f"📋 Gerando relatório completo para {cnpj_fmt}...\n")

        relatorio_gerador = RelatorioCNPJ(buscador=self.buscador)
        relatorio = relatorio_gerador.gerar(cnpj_limpo)

        if "erro" in relatorio:
            print(f"❌ {relatorio['erro']}")
            return

        if output_format == "json":
            print(json.dumps(relatorio, indent=2, ensure_ascii=False))
            if output_file:
                relatorio_gerador.exportar_json(relatorio, output_file)
                print(f"\n✅ Relatório salvo em {output_file}")
        else:
            conteudo = relatorio_gerador.formatar_markdown(relatorio)
            print(conteudo)
            if output_file:
                relatorio_gerador.exportar_markdown(relatorio, output_file)
                print(f"\n✅ Relatório salvo em {output_file}")

    def _exibir_dados(self, dados: Dict, formato: str = "json") -> None:
        """Exibe dados no formato solicitado"""
        if formato == "json":
            print("\n📋 Resultado (JSON):")
            print(json.dumps(dados, indent=2, ensure_ascii=False))

        elif formato == "table":
            print("\n📋 Resultado (Tabela):")
            print("-" * 60)
            for chave, valor in dados.items():
                print(f"{chave:.<30} {valor}")
            print("-" * 60)

        elif formato == "csv":
            print("\n📋 Resultado (CSV):")
            for chave, valor in dados.items():
                print(f"{chave},{valor}")

    def _exportar_resultados(self, resultados: Dict, arquivo: str) -> None:
        """Exporta resultados para arquivo"""
        arquivo_path = self.output_dir / arquivo

        if arquivo.endswith(".json"):
            self.buscador.exportar_json(resultados, str(arquivo_path))
        elif arquivo.endswith(".csv"):
            self.buscador.exportar_csv(resultados, str(arquivo_path))
        else:
            print(f"❌ Formato não suportado: {arquivo}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="CNPJ Explorer - Consulte CNPJs brasileiros",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --validate 11222333000181
  %(prog)s --cnpj 15436940000172
  %(prog)s --csv dados.csv --output resultado.json
  %(prog)s --search "Amazon" --limit 10
        """,
    )

    # Grupos de operações
    parser.add_argument(
        "--version", action="version", version="CNPJ Explorer 1.0.0"
    )

    parser.add_argument(
        "--validate",
        metavar="CNPJ",
        help="Valida um CNPJ",
    )

    parser.add_argument(
        "--cnpj",
        metavar="CNPJ",
        help="Busca informações de um CNPJ",
    )

    parser.add_argument(
        "--csv",
        metavar="ARQUIVO",
        help="Processa arquivo CSV com CNPJs",
    )

    parser.add_argument(
        "--output",
        "-o",
        metavar="ARQUIVO",
        help="Arquivo de saída (JSON/CSV)",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "table", "markdown"],
        default="json",
        help="Formato de saída (padrão: json)",
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Usar processamento paralelo (CSV)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Número de workers para paralelização (padrão: 4)",
    )

    parser.add_argument(
        "--cache",
        action="store_true",
        help="Ativar cache",
    )

    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Limpar cache",
    )

    parser.add_argument(
        "--cache-info",
        action="store_true",
        help="Mostrar informações do cache",
    )

    parser.add_argument(
        "--full",
        metavar="CNPJ",
        help="Relatório completo: sócios + LinkedIn + situação fiscal + Portal da Transparência",
    )

    args = parser.parse_args()

    # Inicializar CLI
    cli = CNPJCLI()

    # Desativar cache se não solicitado
    if not args.cache:
        cli.buscador.cache.clear()

    # Executar operações
    if args.clear_cache:
        cli.limpar_cache()

    elif args.cache_info:
        cli.info_cache()

    elif args.validate:
        cli.validar(args.validate)

    elif args.cnpj:
        cli.buscar_cnpj(args.cnpj, output_format=args.format)

    elif args.full:
        cli.gerar_relatorio_completo(args.full, output_format=args.format, output_file=args.output)

    elif args.csv:
        cli.processar_csv(
            args.csv,
            output_file=args.output,
            paralelo=args.parallel,
            workers=args.workers,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
