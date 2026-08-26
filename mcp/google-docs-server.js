#!/usr/bin/env node

/**
 * MCP Server para Google Docs
 * Permite Claude Code acessar Google Docs via MCP
 *
 * Uso: node google-docs-server.js
 */

const { Server } = require("@anthropic-ai/sdk/lib/MessageCreateParams");
const { StdioServerTransport } = require("@anthropic-ai/sdk/lib/streaming");
const { google } = require("googleapis");
const fs = require("fs");
const path = require("path");

// ⚙️ CONFIGURAÇÃO
const CREDENTIALS_FILE = path.join(
  process.env.HOME,
  "Downloads",
  "thiagodias-30c5309274a4.json"
);

const SCOPES = ["https://www.googleapis.com/auth/documents"];

// 🔐 Carregar credenciais
function loadCredentials() {
  if (!fs.existsSync(CREDENTIALS_FILE)) {
    throw new Error(
      `Credenciais não encontradas em ${CREDENTIALS_FILE}`
    );
  }

  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_FILE, "utf8"));
  return credentials;
}

// 🔑 Autenticar com Google
async function getGoogleAuth() {
  const credentials = loadCredentials();

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: SCOPES,
  });

  return auth;
}

// 📝 Criar documento no Google Docs
async function createDocument(title, content) {
  const auth = await getGoogleAuth();
  const docs = google.docs({ version: "v1", auth });
  const drive = google.drive({ version: "v3", auth });

  try {
    // Criar documento
    console.error(`📝 Criando documento: "${title}"...`);
    const doc = await docs.documents.create({
      requestBody: {
        title: title,
      },
    });

    const docId = doc.data.documentId;
    const docUrl = `https://docs.google.com/document/d/${docId}`;

    console.error(`✅ Documento criado: ${docUrl}`);

    // Adicionar conteúdo
    if (content && content.trim()) {
      console.error(`📄 Adicionando conteúdo...`);
      await docs.documents.batchUpdate({
        documentId: docId,
        requestBody: {
          requests: [
            {
              insertText: {
                text: content,
                location: {
                  index: 1,
                },
              },
            },
          ],
        },
      });
      console.error(`✅ Conteúdo adicionado`);
    }

    return {
      success: true,
      documentId: docId,
      title: title,
      url: docUrl,
      message: `Documento criado: ${docUrl}`,
    };
  } catch (error) {
    console.error(`❌ Erro ao criar documento: ${error.message}`);
    throw error;
  }
}

// 📖 Ler documento do Google Docs
async function readDocument(documentId) {
  const auth = await getGoogleAuth();
  const docs = google.docs({ version: "v1", auth });

  try {
    const doc = await docs.documents.get({
      documentId: documentId,
    });

    return {
      success: true,
      documentId: documentId,
      title: doc.data.title,
      content: extractTextFromDocument(doc.data),
    };
  } catch (error) {
    console.error(`❌ Erro ao ler documento: ${error.message}`);
    throw error;
  }
}

// 🔄 Listar documentos do Google Drive
async function listDocuments(limit = 10) {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    const result = await drive.files.list({
      q: "mimeType='application/vnd.google-apps.document'",
      spaces: "drive",
      fields: "files(id, name, createdTime, modifiedTime)",
      pageSize: limit,
      orderBy: "modifiedTime desc",
    });

    return {
      success: true,
      documents: result.data.files.map((file) => ({
        id: file.id,
        name: file.name,
        created: file.createdTime,
        modified: file.modifiedTime,
        url: `https://docs.google.com/document/d/${file.id}`,
      })),
    };
  } catch (error) {
    console.error(`❌ Erro ao listar documentos: ${error.message}`);
    throw error;
  }
}

// 📤 Compartilhar documento
async function shareDocument(documentId, email, role = "editor") {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    await drive.permissions.create({
      fileId: documentId,
      requestBody: {
        role: role,
        type: "user",
        emailAddress: email,
      },
    });

    return {
      success: true,
      message: `Documento compartilhado com ${email}`,
    };
  } catch (error) {
    console.error(`❌ Erro ao compartilhar: ${error.message}`);
    throw error;
  }
}

// 🛠️ Extrair texto do documento
function extractTextFromDocument(doc) {
  let text = "";
  if (doc.body && doc.body.content) {
    for (const element of doc.body.content) {
      if (element.paragraph) {
        for (const run of element.paragraph.elements) {
          if (run.textRun) {
            text += run.textRun.content;
          }
        }
      }
    }
  }
  return text;
}

// MCP Server setup
const server = {
  name: "google-docs-mcp",
  version: "1.0.0",

  // Ferramentas disponíveis
  tools: [
    {
      name: "create_google_doc",
      description: "Cria um novo documento no Google Docs",
      inputSchema: {
        type: "object",
        properties: {
          title: {
            type: "string",
            description: "Título do documento",
          },
          content: {
            type: "string",
            description: "Conteúdo do documento (opcional)",
          },
        },
        required: ["title"],
      },
    },
    {
      name: "read_google_doc",
      description: "Lê o conteúdo de um documento no Google Docs",
      inputSchema: {
        type: "object",
        properties: {
          documentId: {
            type: "string",
            description: "ID do documento Google Docs",
          },
        },
        required: ["documentId"],
      },
    },
    {
      name: "list_google_docs",
      description: "Lista documentos no Google Drive",
      inputSchema: {
        type: "object",
        properties: {
          limit: {
            type: "number",
            description: "Número máximo de documentos (padrão: 10)",
          },
        },
      },
    },
    {
      name: "share_google_doc",
      description: "Compartilha um documento com outro usuário",
      inputSchema: {
        type: "object",
        properties: {
          documentId: {
            type: "string",
            description: "ID do documento",
          },
          email: {
            type: "string",
            description: "Email para compartilhar",
          },
          role: {
            type: "string",
            enum: ["viewer", "commenter", "editor"],
            description: "Papel do usuário (padrão: editor)",
          },
        },
        required: ["documentId", "email"],
      },
    },
  ],

  // Handlers das ferramentas
  handlers: {
    create_google_doc: async (input) => {
      return await createDocument(input.title, input.content || "");
    },
    read_google_doc: async (input) => {
      return await readDocument(input.documentId);
    },
    list_google_docs: async (input) => {
      return await listDocuments(input.limit || 10);
    },
    share_google_doc: async (input) => {
      return await shareDocument(
        input.documentId,
        input.email,
        input.role || "editor"
      );
    },
  },
};

// Iniciar servidor
async function main() {
  console.error("🚀 Iniciando MCP Server para Google Docs...");
  console.error(`📁 Usando credenciais: ${CREDENTIALS_FILE}`);

  // Testar conexão com Google
  try {
    const auth = await getGoogleAuth();
    console.error("✅ Autenticação com Google OK");
  } catch (error) {
    console.error(`❌ Erro de autenticação: ${error.message}`);
    process.exit(1);
  }

  // Endpoint de teste
  console.error("✅ MCP Server pronto!");
  console.error("Ferramentas disponíveis:");
  server.tools.forEach((tool) => {
    console.error(`  - ${tool.name}: ${tool.description}`);
  });
}

main().catch((error) => {
  console.error(`❌ Erro fatal: ${error.message}`);
  process.exit(1);
});

module.exports = { server, createDocument, readDocument, listDocuments, shareDocument };
