#!/usr/bin/env python3

"""
CNPJ Skill - Integração Python
Exemplos de como usar a skill cnpj-skill em scripts Python
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CNPJSkill:
    """Wrapper Python para cnpj-skill"""

    def __init__(self, skill_path: str = "cnpj-skill"):
        self.skill_path = skill_path
        self._verify_installation()

    def _verify_installation(self) -> bool:
        """Verifica se a skill está instalada"""
        try:
            result = subprocess.run(
                [self.skill_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except FileNotFoundError:
            logger.error(f"cnpj-skill não encontrado em: {self.skill_path}")
            return False

    def _run_skill(self, *args: str) -> tuple[bool, str]:
        """Executa a skill e retorna (sucesso, saída)"""
        try:
            result = subprocess.run(
                [self.skill_path, *args],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout
        except subprocess.TimeoutExpired:
            return False, "Timeout na execução da skill"
        except Exception as e:
            return False, str(e)

    def validate(self, cnpj: str) -> bool:
        """Valida um CNPJ"""
        success, _ = self._run_skill("--validate", cnpj)
        return success

    def query(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Consulta dados de um CNPJ"""
        if not self.validate(cnpj):
            logger.error(f"CNPJ inválido: {cnpj}")
            return None

        success, output = self._run_skill("--cnpj", cnpj)

        if success:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                logger.error("Erro ao decodificar JSON")
                return None
        else:
            logger.error(f"Erro ao consultar CNPJ: {output}")
            return None

    def query_batch(self, cnpjs: List[str]) -> List[Dict[str, Any]]:
        """Consulta múltiplos CNPJs"""
        results = []
        for cnpj in cnpjs:
            data = self.query(cnpj)
            if data:
                results.append(data)
        return results

    def export_excel(self, cnpj: str, output_file: str) -> bool:
        """Exporta dados para Excel"""
        success, output = self._run_skill("--export", cnpj, output_file)
        if success:
            logger.info(f"Arquivo salvo: {output_file}")
        else:
            logger.error(f"Erro ao exportar: {output}")
        return success


# ============================================================================
# Exemplos de Uso
# ============================================================================

def exemplo_1_validacao():
    """Exemplo 1: Validar CNPJs"""
    print("\n📋 Exemplo 1: Validação de CNPJs")
    print("=" * 50)

    skill = CNPJSkill()
    cnpjs = [
        "11222333000181",  # Válido
        "34028316000172",  # Válido
        "99999999999999",  # Inválido
    ]

    for cnpj in cnpjs:
        is_valid = skill.validate(cnpj)
        status = "✓ Válido" if is_valid else "✗ Inválido"
        print(f"{cnpj} - {status}")


def exemplo_2_consulta_simples():
    """Exemplo 2: Consulta simples"""
    print("\n🔍 Exemplo 2: Consulta Simples")
    print("=" * 50)

    skill = CNPJSkill()
    cnpj = "11222333000181"

    data = skill.query(cnpj)

    if data:
        print(f"CNPJ: {data.get('cnpj')}")
        print(f"Razão Social: {data.get('razao_social')}")
        print(f"Situação: {data.get('situacao_cadastral')}")
        print(f"Município: {data.get('municipio')} - {data.get('uf')}")
    else:
        print("Não foi possível consultar o CNPJ")


def exemplo_3_filtrar_dados():
    """Exemplo 3: Filtrar dados específicos"""
    print("\n📊 Exemplo 3: Filtrar Dados Específicos")
    print("=" * 50)

    skill = CNPJSkill()
    cnpjs = ["11222333000181", "34028316000172", "07526847000148"]

    campos = ["cnpj", "razao_social", "municipio", "uf", "situacao_cadastral"]

    print(f"{'CNPJ':<18} {'Razão Social':<30} {'Município':<15} {'UF':<3} {'Situação':<10}")
    print("-" * 80)

    for cnpj in cnpjs:
        data = skill.query(cnpj)
        if data:
            print(
                f"{data.get('cnpj', 'N/A'):<18} "
                f"{data.get('razao_social', 'N/A')[:28]:<30} "
                f"{data.get('municipio', 'N/A')[:13]:<15} "
                f"{data.get('uf', 'N/A'):<3} "
                f"{data.get('situacao_cadastral', 'N/A'):<10}"
            )


def exemplo_4_salvar_json():
    """Exemplo 4: Salvar resultados em JSON"""
    print("\n💾 Exemplo 4: Salvar em JSON")
    print("=" * 50)

    skill = CNPJSkill()
    cnpjs = ["11222333000181", "34028316000172"]

    resultados = []
    for cnpj in cnpjs:
        data = skill.query(cnpj)
        if data:
            resultados.append(data)

    # Salvar em arquivo
    output_file = Path.home() / "cnpj_resultados.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"✓ Dados salvos em: {output_file}")


def exemplo_5_processar_lote():
    """Exemplo 5: Processar lote de CNPJs"""
    print("\n📑 Exemplo 5: Processamento em Lote")
    print("=" * 50)

    skill = CNPJSkill()

    # Criar arquivo de entrada
    input_file = Path.home() / "cnpjs_para_consultar.txt"
    cnpjs = [
        "11222333000181",
        "34028316000172",
        "07526847000148",
    ]

    with open(input_file, "w") as f:
        for cnpj in cnpjs:
            f.write(cnpj + "\n")

    print(f"Arquivo criado: {input_file}")
    print(f"Consultando {len(cnpjs)} CNPJs...")

    resultados = skill.query_batch(cnpjs)

    print(f"✓ {len(resultados)} CNPJs consultados com sucesso")


def exemplo_6_filtro_por_estado():
    """Exemplo 6: Filtrar empresas por estado"""
    print("\n🗺️  Exemplo 6: Filtrar por Estado")
    print("=" * 50)

    skill = CNPJSkill()
    cnpjs = ["11222333000181", "34028316000172", "07526847000148"]

    # Agrupar por estado
    por_estado = {}

    for cnpj in cnpjs:
        data = skill.query(cnpj)
        if data:
            uf = data.get("uf", "N/A")
            if uf not in por_estado:
                por_estado[uf] = []
            por_estado[uf].append(data["razao_social"])

    print("\nEmpresas por estado:")
    for uf, empresas in sorted(por_estado.items()):
        print(f"\n{uf}:")
        for empresa in empresas:
            print(f"  - {empresa}")


def exemplo_7_tratamento_erros():
    """Exemplo 7: Tratamento robusto de erros"""
    print("\n⚠️  Exemplo 7: Tratamento de Erros")
    print("=" * 50)

    skill = CNPJSkill()

    testes = [
        ("11222333000181", "CNPJ válido"),
        ("99999999999999", "CNPJ inválido"),
        ("", "CNPJ vazio"),
        ("abc", "CNPJ inválido"),
    ]

    for cnpj, descricao in testes:
        print(f"\nTestando: {descricao}")
        try:
            if skill.validate(cnpj):
                data = skill.query(cnpj)
                if data:
                    print(f"  ✓ Dados obtidos: {data.get('razao_social', 'N/A')}")
                else:
                    print("  ! CNPJ não encontrado na base")
            else:
                print("  ✗ CNPJ inválido")
        except Exception as e:
            print(f"  ✗ Erro: {e}")


# ============================================================================
# Main
# ============================================================================

def main():
    """Executa todos os exemplos"""
    print("🚀 CNPJ Skill - Exemplos de Integração Python")
    print("=" * 50)

    try:
        exemplo_1_validacao()
        exemplo_2_consulta_simples()
        exemplo_3_filtrar_dados()
        exemplo_4_salvar_json()
        exemplo_5_processar_lote()
        exemplo_6_filtro_por_estado()
        exemplo_7_tratamento_erros()

        print("\n" + "=" * 50)
        print("✓ Todos os exemplos foram executados!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
