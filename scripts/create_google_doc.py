#!/usr/bin/env python3
"""
Script para criar documento no Google Docs automaticamente
Usa credenciais locais (Service Account JSON)

Uso:
    python create_google_doc.py "Título do Doc" "Conteúdo aqui"
"""

import json
import sys
import os
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ⚙️ CONFIGURAÇÃO
CREDENTIALS_FILE = Path.home() / "Downloads" / "thiagodias-30c5309274a4.json"
SCOPES = ['https://www.googleapis.com/auth/documents']

def load_credentials():
    """Carrega credenciais da Service Account"""
    if not CREDENTIALS_FILE.exists():
        print(f"❌ Erro: Arquivo de credenciais não encontrado em {CREDENTIALS_FILE}")
        print("   Coloque o arquivo JSON de Service Account naquele local.")
        sys.exit(1)

    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )
    return credentials

def create_document(title, content, share_email=None):
    """
    Cria documento no Google Docs

    Args:
        title: Título do documento
        content: Conteúdo do documento
        share_email: Email para compartilhar (opcional)

    Returns:
        URL do documento criado
    """
    try:
        # Autenticar
        credentials = load_credentials()
        docs_service = build('docs', 'v1')
        drive_service = build('drive', 'v3', credentials=credentials)

        # Criar documento
        print(f"📝 Criando documento: '{title}'...")
        doc_body = {'title': title}
        doc = docs_service.documents().create(body=doc_body).execute()
        doc_id = doc.get('documentId')
        doc_url = f"https://docs.google.com/document/d/{doc_id}"

        print(f"✅ Documento criado: {doc_url}")

        # Adicionar conteúdo
        if content:
            print(f"📄 Adicionando conteúdo ({len(content)} caracteres)...")
            requests = [
                {
                    'insertText': {
                        'text': content,
                        'location': {'index': 1}
                    }
                }
            ]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            print("✅ Conteúdo adicionado")

        # Compartilhar (opcional)
        if share_email:
            print(f"🔗 Compartilhando com {share_email}...")
            drive_service.permissions().create(
                fileId=doc_id,
                body={
                    'type': 'user',
                    'role': 'editor',
                    'emailAddress': share_email
                },
                fields='id'
            ).execute()
            print("✅ Compartilhado")

        print(f"\n🎉 Sucesso! Acesse: {doc_url}\n")
        return doc_url

    except HttpError as error:
        print(f"❌ Erro Google API: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"❌ Erro: {error}")
        sys.exit(1)

def main():
    """Função principal"""

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("❌ Uso: python create_google_doc.py <título> [conteúdo] [email-para-compartilhar]")
        print("\nExemplos:")
        print('  python create_google_doc.py "Meu Documento"')
        print('  python create_google_doc.py "Trix" "Análise de mercado aqui"')
        print('  python create_google_doc.py "Trix" "Conteúdo" "friend@gmail.com"')
        sys.exit(1)

    title = sys.argv[1]
    content = sys.argv[2] if len(sys.argv) > 2 else ""
    share_email = sys.argv[3] if len(sys.argv) > 3 else None

    # Criar documento
    create_document(title, content, share_email)

if __name__ == '__main__':
    main()
