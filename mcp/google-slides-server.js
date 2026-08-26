#!/usr/bin/env node

/**
 * MCP Server para Google Slides (PowerPoint)
 * Permite Claude Code criar/editar apresentações
 */

const { google } = require("googleapis");
const fs = require("fs");
const path = require("path");

const CREDENTIALS_FILE = path.join(
  process.env.HOME,
  "Downloads",
  "thiagodias-30c5309274a4.json"
);

const SCOPES = [
  "https://www.googleapis.com/auth/presentations",
  "https://www.googleapis.com/auth/drive",
];

function loadCredentials() {
  if (!fs.existsSync(CREDENTIALS_FILE)) {
    throw new Error(`Credenciais não encontradas em ${CREDENTIALS_FILE}`);
  }
  return JSON.parse(fs.readFileSync(CREDENTIALS_FILE, "utf8"));
}

async function getGoogleAuth() {
  const credentials = loadCredentials();
  return new google.auth.GoogleAuth({
    credentials,
    scopes: SCOPES,
  });
}

// 📊 Criar apresentação
async function createPresentation(title) {
  const auth = await getGoogleAuth();
  const slides = google.slides({ version: "v1", auth });

  try {
    console.error(`📊 Criando apresentação: "${title}"...`);

    const presentation = await slides.presentations.create({
      requestBody: {
        title: title,
      },
    });

    const presentationId = presentation.data.presentationId;
    const presentationUrl = `https://docs.google.com/presentation/d/${presentationId}`;

    console.error(`✅ Apresentação criada: ${presentationUrl}`);

    return {
      success: true,
      presentationId: presentationId,
      title: title,
      url: presentationUrl,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// ➕ Adicionar slide
async function addSlide(presentationId, title, content) {
  const auth = await getGoogleAuth();
  const slides = google.slides({ version: "v1", auth });

  try {
    const presentation = await slides.presentations.get({
      presentationId: presentationId,
    });

    const pageId = `page_${Date.now()}`;

    const requests = [
      {
        createSlide: {
          objectId: pageId,
          insertIndex: presentation.data.slides.length,
          slideLayout: {
            predefinedLayout: "BLANK",
          },
        },
      },
      {
        insertText: {
          objectId: pageId,
          text: title,
          insertionIndex: 0,
        },
      },
    ];

    if (content) {
      requests.push({
        insertText: {
          objectId: pageId,
          text: "\n" + content,
          insertionIndex: title.length,
        },
      });
    }

    await slides.presentations.batchUpdate({
      presentationId: presentationId,
      requestBody: { requests },
    });

    console.error(`✅ Slide adicionado`);

    return {
      success: true,
      pageId: pageId,
      message: "Slide adicionado com sucesso",
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 🔗 Compartilhar apresentação
async function sharePresentation(presentationId, email, role = "editor") {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    await drive.permissions.create({
      fileId: presentationId,
      requestBody: {
        role: role,
        type: "user",
        emailAddress: email,
      },
    });

    console.error(`✅ Apresentação compartilhada com ${email}`);

    return {
      success: true,
      message: `Apresentação compartilhada com ${email}`,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

module.exports = {
  createPresentation,
  addSlide,
  sharePresentation,
};
