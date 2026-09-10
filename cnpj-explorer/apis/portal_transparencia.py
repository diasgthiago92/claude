import os
import requests
from typing import Optional, List, Dict


class ClientePortalTransparencia:
    """Cliente para a API oficial e gratuita do Portal da Transparência."""

    BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"

    def __init__(self, token: Optional[str] = None, timeout: int = 10):
        self.token = token or os.getenv("PORTAL_TRANSPARENCIA_API_TOKEN", "").strip()
        self.timeout = timeout

    def configurado(self) -> bool:
        return bool(self.token)

    def _headers(self) -> Dict[str, str]:
        return {"chave-api-dados": self.token}

    def buscar_contratos(self, cnpj_formatado: str, pagina: int = 1) -> List[Dict]:
        """
        GET /contratos/cpf-cnpj?cpfCnpj=<cnpj_formatado>&pagina=<pagina>
        Retorna [] em erro/sem token (nunca lança).
        """
        if not self.configurado():
            return []

        try:
            url = f"{self.BASE_URL}/contratos/cpf-cnpj"
            params = {"cpfCnpj": cnpj_formatado, "pagina": pagina}
            response = requests.get(
                url,
                headers=self._headers(),
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return []

    def buscar_sancoes(self, cnpj_formatado: str) -> Dict[str, List[Dict]]:
        """
        Consulta /ceis?codigoSancionado=... e /cnep?codigoSancionado=...
        para buscar sanções (CEIS: Cadastro de Entidades Inidôneas, CNEP: Cadastro Nacional de Empresas Punidas).
        Retorna {"ceis": [...], "cnep": [...]}.
        """
        if not self.configurado():
            return {"ceis": [], "cnep": []}

        resultado = {"ceis": [], "cnep": []}

        try:
            params = {"codigoSancionado": cnpj_formatado.replace(".", "").replace("-", "").replace("/", "")}

            for endpoint in ["ceis", "cnep"]:
                try:
                    url = f"{self.BASE_URL}/{endpoint}"
                    response = requests.get(
                        url,
                        headers=self._headers(),
                        params=params,
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    resultado[endpoint] = response.json()
                except requests.exceptions.RequestException:
                    resultado[endpoint] = []

        except Exception:
            pass

        return resultado

    @staticmethod
    def mensagem_nao_configurado() -> str:
        return (
            "🔑 Consulta ao Portal da Transparência desativada: configure PORTAL_TRANSPARENCIA_API_TOKEN\n"
            "   Cadastro gratuito: https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email"
        )
