import os
import requests
from typing import Optional, List, Dict


class BuscadorLinkedIn:
    """Busca candidatos a perfis LinkedIn via Google Custom Search (não scraping direto)."""

    GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        cse_id: Optional[str] = None,
        max_resultados: int = 3,
        timeout: int = 5
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "").strip()
        self.cse_id = cse_id or os.getenv("GOOGLE_CSE_ID", "").strip()
        self.max_resultados = max_resultados
        self.timeout = timeout

    def configurado(self) -> bool:
        return bool(self.api_key and self.cse_id)

    def buscar_candidatos(self, nome_socio: str) -> List[Dict]:
        """
        Faz UMA query '"<nome_socio>" linkedin' e filtra itens cujo link
        contenha 'linkedin.com/in/'. Retorna [] se não configurado, sem
        resultados, ou em erro de rede/HTTP (nunca lança exceção).
        Cada item: {"titulo": str, "link": str, "snippet": str}.
        """
        if not self.configurado():
            return []

        try:
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": f'"{nome_socio}" linkedin',
                "num": min(self.max_resultados, 10)
            }
            response = requests.get(
                self.GOOGLE_CSE_URL,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 429:
                return []

            response.raise_for_status()
            data = response.json()

            items = []
            for item in data.get("items", []):
                if "linkedin.com/in/" in item.get("link", "").lower():
                    items.append({
                        "titulo": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })

            return items[:self.max_resultados]

        except requests.exceptions.RequestException:
            return []

    def buscar_para_socios(self, socios_qsa: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Itera sobre sócios PESSOA FÍSICA do QSA (identificador_de_socio == 1;
        pula PJ/estrangeiro), chama buscar_candidatos(nome_socio) para cada um.
        Se detectar erro HTTP 429 (quota diária excedida), para o loop.
        Retorna {nome_socio: [candidatos]}.
        """
        resultado = {}

        for socio in socios_qsa:
            if socio.get("identificador_de_socio") != 1:
                continue

            nome = socio.get("nome_socio", "").strip()
            if not nome:
                continue

            candidatos = self.buscar_candidatos(nome)
            resultado[nome] = candidatos

            if not candidatos and len(resultado) > 0:
                break

        return resultado

    @staticmethod
    def mensagem_nao_configurado() -> str:
        return (
            "🔑 Busca de LinkedIn desativada: configure GOOGLE_API_KEY e GOOGLE_CSE_ID\n"
            "   Cadastro gratuito (100 buscas/dia): "
            "https://developers.google.com/custom-search/v1/overview"
        )
