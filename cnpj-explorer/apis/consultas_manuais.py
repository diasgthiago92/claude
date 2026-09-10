from typing import List, Dict


def gerar_links_consulta_manual(cnpj_formatado: str) -> List[Dict[str, str]]:
    """
    Gera links diretos para consultas que exigem CAPTCHA/login.
    Cada item: {"nome": str, "url": str, "observacao": str}.
    """
    cnpj_limpo = cnpj_formatado.replace(".", "").replace("-", "").replace("/", "")

    return [
        {
            "nome": "CND Federal (Receita Federal/PGFN)",
            "url": f"https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir?tipo=1&origem=header&cnpj={cnpj_limpo}",
            "observacao": "Consulta manual - requer CAPTCHA"
        },
        {
            "nome": "CNDT (Débitos Trabalhistas - TST)",
            "url": "https://cndt-certidao.tst.jus.br/inicio.faces",
            "observacao": "Consulta manual - requer busca por CNPJ no sistema"
        },
        {
            "nome": "Protestos em Cartório",
            "url": f"https://www.google.com/search?q=protesto+cnpj+{cnpj_limpo}",
            "observacao": "Sem portal nacional único - varia por estado (IEPTB-SP, etc)"
        }
    ]
