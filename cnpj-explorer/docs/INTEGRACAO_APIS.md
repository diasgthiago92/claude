# Integração com APIs 🔌

Guia completo para integrar diferentes fontes de dados de CNPJ em seu projeto.

---

## 1. BrasilAPI (Recomendada para Começar)

**Documentação:** https://brasilapi.com.br/

### Características
- ✅ Gratuita
- ✅ Sem autenticação
- ✅ Dados atualizados
- ✅ Fácil de usar
- ⚠️ Rate limit: ~50 req/min

### Instalação

```bash
pip install requests
```

### Uso Básico (Python)

```python
import requests

def buscar_cnpj(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    response = requests.get(url)
    return response.json()

# Usar
dados = buscar_cnpj("11222333000181")
print(dados)
```

### Resposta Esperada

```json
{
  "cnpj": "11222333000181",
  "razao_social": "FAKE EMPRESA S.A.",
  "logradouro": "RUA FAKE",
  "numero": "123",
  "complemento": "APTO 456",
  "bairro": "CENTRO",
  "municipio": "SAO PAULO",
  "uf": "SP",
  "cep": "01310100",
  "natureza_juridica": "Sociedade Empresária",
  "telefone": "1133334444"
}
```

### Tratamento de Erros

```python
import requests
from requests.exceptions import RequestException

def buscar_cnpj_seguro(cnpj):
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Erro na API: {e}")
        return None
```

### Com Cache

```python
import requests
from functools import lru_cache
from datetime import datetime, timedelta

cache_time = {}

@lru_cache(maxsize=100)
def buscar_cnpj_cache(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    response = requests.get(url)
    cache_time[cnpj] = datetime.now()
    return response.json()

# Limpar cache antigo (>24h)
def limpar_cache():
    agora = datetime.now()
    for cnpj in list(cache_time.keys()):
        if agora - cache_time[cnpj] > timedelta(hours=24):
            buscar_cnpj_cache.cache_clear()
```

---

## 2. Receita Federal (Dados Oficiais)

**Fonte:** https://www.gov.br/pt-br/servicos/consultar-dados-cadastrais-da-empresa

### Características
- ✅ Fonte oficial
- ✅ Dados completíssimos
- ✅ Atualização diária
- ✅ Gratuita
- ⚠️ Formato XML complexo
- ⚠️ Requer download de arquivo grande (~100MB)

### Instalação

```bash
pip install lxml pandas
```

### Downloading Dados

```python
import urllib.request
import os

def download_receita_federal():
    url = "https://www.gov.br/pt-br/servicos/consultar-dados-cadastrais-da-empresa"
    # URL direto para download (verificar site)
    # Tipicamente em: https://www8.receita.fazenda.gov.br/CNPJ/
    
    arquivo = "cnpj.zip"
    print(f"Baixando {arquivo}...")
    urllib.request.urlretrieve(url, arquivo)
    print("Download concluído!")
```

### Parsing XML

```python
from lxml import etree
import zipfile

def extrair_cnpj_receita(cnpj):
    # Descompactar arquivo
    with zipfile.ZipFile('cnpj.zip', 'r') as zip_ref:
        zip_ref.extractall('data/')
    
    # Procurar CNPJ
    for file in os.listdir('data/'):
        if file.endswith('.xml'):
            tree = etree.parse(f'data/{file}')
            root = tree.getroot()
            
            for empresa in root.findall('.//empresa'):
                cnpj_elem = empresa.find('cnpj')
                if cnpj_elem is not None and cnpj_elem.text == cnpj:
                    return {
                        'cnpj': empresa.find('cnpj').text,
                        'razao_social': empresa.find('razao_social').text,
                        'endereco': empresa.find('endereco').text,
                    }
    return None
```

---

## 3. Serenata de Amor (Análise de Integridade)

**GitHub:** https://github.com/serenata/serenata-de-amor

### Características
- ✅ Análise de integridade
- ✅ Dados públicos ligados a licitações
- ✅ Comunidade ativa
- ✅ Dados atualizados
- ⚠️ Foco em análise, não só busca

### Instalação

```bash
pip install serenata-toolbelt
```

### Uso

```python
from serenata_toolbelt import datasets

# Buscar dados
companies = datasets.fetch('serenata-companies')

# Filtrar por CNPJ
cnpj_procurado = "11222333000181"
empresa = companies[companies['cnpj'] == cnpj_procurado]

if not empresa.empty:
    print(empresa[['name', 'cnpj', 'status', 'founded']])
```

### Análise Completa

```python
from serenata_toolbelt import datasets

def analisar_empresa(cnpj):
    # Dados básicos
    companies = datasets.fetch('serenata-companies')
    empresa = companies[companies['cnpj'] == cnpj].iloc[0]
    
    print(f"Empresa: {empresa['name']}")
    print(f"Status: {empresa['status']}")
    print(f"Fundação: {empresa['founded']}")
    
    # Procurar problemas
    if empresa['status'] != 'ATIVA':
        print("⚠️ Empresa não está ativa!")
    
    return empresa

# Usar
analisar_empresa("11222333000181")
```

---

## 4. Meu CNPJ (API Paga - Dados em Tempo Real)

**Site:** https://www.meucnpj.com/api

### Características
- ✅ Dados em tempo real
- ✅ Dados muito completos
- ✅ Suporte técnico
- ✅ Taxa de sucesso alta
- ❌ Pago (créditos)

### Instalação

```bash
pip install meucnpj-api
```

### Uso com Autenticação

```python
import requests

API_KEY = "sua_chave_aqui"

def buscar_cnpj_meucnpj(cnpj):
    url = f"https://www.meucnpj.com/api/v1/cnpj/{cnpj}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

# Usar
dados = buscar_cnpj_meucnpj("11222333000181")
print(dados)
```

---

## 5. Comparação de APIs

| API | Custo | Autenticação | Dados | Velocidade | Atualização |
|-----|-------|--------------|-------|-----------|-------------|
| BrasilAPI | Gratuita | Não | Básicos | Rápida | Semanal |
| Receita Federal | Gratuita | Não | Completos | Lenta | Diária |
| Serenata | Gratuita | Não | Análise | Média | Mensal |
| Meu CNPJ | Paga | Sim | Completos | Rápida | Tempo real |

---

## 6. Implementação Múltiplas Fontes

```python
class BuscadorCNPJ:
    def __init__(self):
        self.fonte_primaria = "brasilapi"
        self.fonte_fallback = "serenata"
    
    def buscar(self, cnpj):
        # Tentar primeira fonte
        try:
            return self._brasilapi(cnpj)
        except Exception as e:
            print(f"BrasilAPI falhou: {e}")
            
            # Tentar fallback
            try:
                return self._serenata(cnpj)
            except Exception as e2:
                print(f"Serenata falhou: {e2}")
                return None
    
    def _brasilapi(self, cnpj):
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
    def _serenata(self, cnpj):
        from serenata_toolbelt import datasets
        companies = datasets.fetch('serenata-companies')
        empresa = companies[companies['cnpj'] == cnpj].iloc[0]
        return empresa.to_dict()

# Usar
buscador = BuscadorCNPJ()
dados = buscador.buscar("11222333000181")
```

---

## 7. Rate Limiting e Throttling

```python
import time
from datetime import datetime, timedelta

class ThrottledAPI:
    def __init__(self, requests_per_second=10):
        self.rpm = requests_per_second
        self.last_request = datetime.now()
        self.requests = []
    
    def esperar(self):
        agora = datetime.now()
        
        # Remover requisições antigas
        self.requests = [
            r for r in self.requests 
            if agora - r < timedelta(seconds=60)
        ]
        
        # Se muitas requisições, esperar
        if len(self.requests) >= self.rpm:
            tempo_espera = 60 - (agora - self.requests[0]).total_seconds()
            if tempo_espera > 0:
                print(f"Rate limit atingido. Esperando {tempo_espera:.1f}s...")
                time.sleep(tempo_espera)
        
        self.requests.append(agora)
    
    def buscar(self, cnpj):
        self.esperar()
        # Fazer requisição
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        return requests.get(url).json()

# Usar
api = ThrottledAPI(requests_per_second=5)
dados = api.buscar("11222333000181")
```

---

## 8. Variáveis de Ambiente

Arquivo: `.env`

```env
# BrasilAPI
BRASILAPI_URL=https://brasilapi.com.br/api/cnpj/v1/
BRASILAPI_TIMEOUT=5

# Meu CNPJ
MEUCNPJ_API_KEY=sua_chave
MEUCNPJ_URL=https://www.meucnpj.com/api/v1/

# Cache
CACHE_ENABLED=true
CACHE_TTL=86400

# Logging
LOG_LEVEL=INFO
```

Usar:

```python
import os
from dotenv import load_dotenv

load_dotenv()

BRASILAPI_URL = os.getenv("BRASILAPI_URL")
MEUCNPJ_API_KEY = os.getenv("MEUCNPJ_API_KEY")
```

---

**Última atualização:** 2026-09-09
