import json
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.brasilapi_integration import BuscadorBrasilAPI
from apis.linkedin_search import BuscadorLinkedIn
from apis.portal_transparencia import ClientePortalTransparencia
from apis.consultas_manuais import gerar_links_consulta_manual


class RelatorioCNPJ:
    def __init__(
        self,
        buscador: Optional[BuscadorBrasilAPI] = None,
        linkedin: Optional[BuscadorLinkedIn] = None,
        transparencia: Optional[ClientePortalTransparencia] = None
    ):
        self.buscador = buscador or BuscadorBrasilAPI()
        self.linkedin = linkedin or BuscadorLinkedIn()
        self.transparencia = transparencia or ClientePortalTransparencia()

    def gerar(
        self,
        cnpj: str,
        incluir_linkedin: bool = True,
        incluir_transparencia: bool = True
    ) -> Dict:
        """
        Pipeline completo: valida CNPJ, busca dados na BrasilAPI, extrai sócios,
        opcionalmente busca LinkedIn e Portal da Transparência, monta situação fiscal.
        Retorna dict único com "avisos" para qualquer falha (nunca lança exceção).
        """
        avisos = []

        cnpj_limpo = cnpj.replace(".", "").replace("-", "").replace("/", "")

        if not (len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()):
            return {"erro": f"CNPJ inválido: {cnpj}"}

        cnpj_formatado = self._formatar_cnpj(cnpj_limpo)

        dados = self.buscador.buscar(cnpj_limpo)
        if not dados:
            return {"erro": "CNPJ não encontrado na BrasilAPI"}

        socios = self._extrair_socios(dados.get("qsa", []))

        linkedin_resultados = {}
        if incluir_linkedin:
            if self.linkedin.configurado():
                linkedin_resultados = self.linkedin.buscar_para_socios(socios)
            else:
                avisos.append(BuscadorLinkedIn.mensagem_nao_configurado())

        situacao_fiscal = self._montar_situacao_fiscal(
            dados,
            cnpj_formatado,
            cnpj_limpo,
            incluir_transparencia,
            avisos
        )

        for socio in socios:
            nome = socio.get("nome")
            if nome and nome in linkedin_resultados:
                socio["linkedin_candidatos"] = linkedin_resultados[nome]

        relatorio = {
            "cnpj": cnpj_formatado,
            "razao_social": dados.get("razao_social", ""),
            "nome_fantasia": dados.get("nome_fantasia", ""),
            "porte": dados.get("porte", ""),
            "situacao_cadastral": {
                "situacao": dados.get("descricao_situacao_cadastral", ""),
                "data": dados.get("data_situacao_cadastral", ""),
                "motivo": dados.get("descricao_motivo_situacao_cadastral", "")
            },
            "endereco": {
                "logradouro": dados.get("logradouro", ""),
                "numero": dados.get("numero", ""),
                "complemento": dados.get("complemento", ""),
                "bairro": dados.get("bairro", ""),
                "cep": dados.get("cep", ""),
                "municipio": dados.get("municipio", ""),
                "uf": dados.get("uf", "")
            },
            "atividade_principal": {
                "codigo": dados.get("cnae_fiscal", ""),
                "descricao": dados.get("cnae_fiscal_descricao", "")
            },
            "atividades_secundarias": [
                {
                    "codigo": cnae.get("codigo", ""),
                    "descricao": cnae.get("descricao", "")
                }
                for cnae in dados.get("cnaes_secundarios", [])
            ][:10],
            "capital_social": dados.get("capital_social", 0),
            "regime_tributario": [
                {
                    "ano": rt.get("ano", ""),
                    "forma": rt.get("forma_de_tributacao", ""),
                    "escrituracoes": rt.get("quantidade_de_escrituracoes", 0)
                }
                for rt in dados.get("regime_tributario", [])
            ],
            "socios": socios,
            "situacao_fiscal": situacao_fiscal,
            "contatos": {
                "telefone": dados.get("ddd_telefone_1", ""),
                "email": dados.get("email", "")
            },
            "avisos": avisos,
            "gerado_em": datetime.now().isoformat()
        }

        return relatorio

    def _formatar_cnpj(self, cnpj_limpo: str) -> str:
        """Formata CNPJ para XX.XXX.XXX/XXXX-XX"""
        if len(cnpj_limpo) != 14:
            return cnpj_limpo
        return f"{cnpj_limpo[0:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:14]}"

    def _extrair_socios(self, qsa: List[Dict]) -> List[Dict]:
        """
        Normaliza sócios do QSA bruto da BrasilAPI para formato legível.
        Mantém campos públicos: nome, cpf_cnpj_mascarado, qualificacao, faixa_etaria,
        data_entrada_sociedade, tipo (PF/PJ/Estrangeiro), pais (se houver).
        """
        socios_norm = []

        for socio in qsa:
            tipo = "Pessoa Jurídica Domiciliado no Exterior"
            if socio.get("identificador_de_socio") == 1:
                tipo = "Pessoa Física"
            elif socio.get("identificador_de_socio") == 2:
                tipo = "Pessoa Jurídica"

            socio_norm = {
                "nome": socio.get("nome_socio", ""),
                "cpf_cnpj_mascarado": socio.get("cnpj_cpf_do_socio", ""),
                "qualificacao": socio.get("qualificacao_socio", ""),
                "faixa_etaria": socio.get("faixa_etaria", "Não se aplica"),
                "data_entrada_sociedade": socio.get("data_entrada_sociedade", ""),
                "tipo": tipo,
                "identificador_de_socio": socio.get("identificador_de_socio", 0)
            }

            if socio.get("pais"):
                socio_norm["pais"] = socio.get("pais")

            if socio.get("nome_representante_legal"):
                socio_norm["representante_legal"] = socio.get("nome_representante_legal")

            socios_norm.append(socio_norm)

        return socios_norm

    def _montar_situacao_fiscal(
        self,
        dados: Dict,
        cnpj_formatado: str,
        cnpj_limpo: str,
        incluir_transparencia: bool,
        avisos: List[str]
    ) -> Dict:
        """
        Consolida situação fiscal: cadastral, Portal da Transparência, consultas manuais.
        """
        situacao_fiscal = {
            "situacao_cadastral": dados.get("descricao_situacao_cadastral", ""),
            "data_situacao_cadastral": dados.get("data_situacao_cadastral", ""),
            "portal_transparencia": None,
            "consultas_manuais": gerar_links_consulta_manual(cnpj_formatado)
        }

        if incluir_transparencia:
            if self.transparencia.configurado():
                contratos = self.transparencia.buscar_contratos(cnpj_formatado)
                sancoes = self.transparencia.buscar_sancoes(cnpj_formatado)
                situacao_fiscal["portal_transparencia"] = {
                    "contratos": contratos,
                    "sancoes": sancoes
                }
            else:
                avisos.append(ClientePortalTransparencia.mensagem_nao_configurado())

        return situacao_fiscal

    def formatar_markdown(self, relatorio: Dict) -> str:
        """Gera texto Markdown legível."""
        if "erro" in relatorio:
            return f"❌ Erro: {relatorio['erro']}"

        linhas = []
        linhas.append(f"# CNPJ: {relatorio['cnpj']}")
        linhas.append("")
        linhas.append(f"**Razão Social**: {relatorio['razao_social']}")
        linhas.append(f"**Situação**: {relatorio['situacao_cadastral']['situacao']}")
        linhas.append(f"**Porte**: {relatorio['porte']}")
        linhas.append("")

        linhas.append("## 📍 Endereço")
        endereco = relatorio["endereco"]
        linhas.append(
            f"{endereco['logradouro']}, {endereco['numero']} {endereco['complemento']} "
            f"- {endereco['bairro']} - {endereco['municipio']}/{endereco['uf']} "
            f"CEP {endereco['cep']}"
        )
        linhas.append("")

        linhas.append("## 💼 Atividade")
        atividade = relatorio["atividade_principal"]
        linhas.append(f"- **Principal**: ({atividade['codigo']}) {atividade['descricao']}")
        if relatorio["atividades_secundarias"]:
            linhas.append("- **Secundárias**:")
            for sec in relatorio["atividades_secundarias"]:
                linhas.append(f"  - ({sec['codigo']}) {sec['descricao']}")
        linhas.append("")

        linhas.append("## 💰 Financeiro")
        linhas.append(f"- **Capital Social**: R$ {relatorio['capital_social']:,.2f}".replace(",", "."))
        if relatorio["regime_tributario"]:
            linhas.append("- **Regime Tributário**:")
            for rt in relatorio["regime_tributario"][-3:]:
                linhas.append(f"  - {rt['ano']}: {rt['forma']}")
        linhas.append("")

        linhas.append("## 👥 Sócios")
        if relatorio["socios"]:
            for socio in relatorio["socios"]:
                linhas.append(f"- **{socio['nome']}** ({socio['tipo']})")
                linhas.append(f"  - CPF/CNPJ: {socio['cpf_cnpj_mascarado']}")
                linhas.append(f"  - Cargo: {socio['qualificacao']}")
                linhas.append(f"  - Desde: {socio['data_entrada_sociedade']}")
                if socio.get("faixa_etaria") != "Não se aplica":
                    linhas.append(f"  - Idade: {socio['faixa_etaria']}")

                if socio.get("linkedin_candidatos"):
                    linhas.append("  - **Candidatos LinkedIn**:")
                    for cand in socio["linkedin_candidatos"]:
                        linhas.append(f"    - [{cand['titulo']}]({cand['link']})")
                    linhas.append("    ⚠️ Confirme manualmente — nomes comuns geram falsos positivos")
        else:
            linhas.append("Nenhum sócio registrado")
        linhas.append("")

        linhas.append("## 📋 Situação Fiscal")
        linhas.append(f"- **Cadastral**: {relatorio['situacao_cadastral']['situacao']}")
        linhas.append(f"  (desde {relatorio['situacao_cadastral']['data']})")

        if relatorio["situacao_fiscal"]["portal_transparencia"]:
            pt = relatorio["situacao_fiscal"]["portal_transparencia"]
            linhas.append("- **Portal da Transparência**:")
            contratos = pt.get("contratos", [])
            sancoes = pt.get("sancoes", {})
            linhas.append(f"  - Contratos: {len(contratos) if isinstance(contratos, list) else 0}")
            ceis = sancoes.get("ceis", []) if isinstance(sancoes, dict) else []
            cnep = sancoes.get("cnep", []) if isinstance(sancoes, dict) else []
            linhas.append(f"  - Sanções (CEIS): {len(ceis) if isinstance(ceis, list) else 0}")
            linhas.append(f"  - Sanções (CNEP): {len(cnep) if isinstance(cnep, list) else 0}")
        else:
            linhas.append("- **Portal da Transparência**: Não consultado")

        linhas.append("")
        linhas.append("### 🔗 Consultas Manuais Necessárias")
        for consulta in relatorio["situacao_fiscal"]["consultas_manuais"]:
            linhas.append(f"- [{consulta['nome']}]({consulta['url']})")
            linhas.append(f"  _{consulta['observacao']}_")

        linhas.append("")

        if relatorio["avisos"]:
            linhas.append("### ⚠️ Avisos")
            for aviso in relatorio["avisos"]:
                linhas.append(f"> {aviso}")
            linhas.append("")

        linhas.append(f"_Gerado em {relatorio['gerado_em']}_")

        return "\n".join(linhas)

    def exportar_json(self, relatorio: Dict, caminho: str) -> None:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)

    def exportar_markdown(self, relatorio: Dict, caminho: str) -> None:
        conteudo = self.formatar_markdown(relatorio)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
