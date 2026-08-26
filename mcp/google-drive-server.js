#!/usr/bin/env node

/**
 * MCP Server para Google Drive
 * Gerenciar arquivos, pastas, uploads
 */

const { google } = require("googleapis");
const fs = require("fs");
const path = require("path");

const CREDENTIALS_FILE = path.join(
  process.env.HOME,
  "Downloads",
  "thiagodias-30c5309274a4.json"
);

const SCOPES = ["https://www.googleapis.com/auth/drive"];

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

// 📁 Listar arquivos
async function listFiles(query = null, limit = 20) {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    const q = query || "trashed = false";

    const result = await drive.files.list({
      q: q,
      spaces: "drive",
      fields: "files(id, name, mimeType, createdTime, modifiedTime, webViewLink)",
      pageSize: limit,
      orderBy: "modifiedTime desc",
    });

    return {
      success: true,
      files: result.data.files.map((file) => ({
        id: file.id,
        name: file.name,
        type: file.mimeType,
        created: file.createdTime,
        modified: file.modifiedTime,
        url: file.webViewLink,
      })),
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 📤 Upload de arquivo
async function uploadFile(filePath, fileName, parentFolderId = null) {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    if (!fs.existsSync(filePath)) {
      throw new Error(`Arquivo não encontrado: ${filePath}`);
    }

    console.error(`📤 Fazendo upload de ${fileName}...`);

    const fileMetadata = {
      name: fileName,
    };

    if (parentFolderId) {
      fileMetadata.parents = [parentFolderId];
    }

    const media = {
      body: fs.createReadStream(filePath),
    };

    const file = await drive.files.create({
      resource: fileMetadata,
      media: media,
      fields: "id, webViewLink",
    });

    const fileId = file.data.id;
    const fileUrl = file.data.webViewLink;

    console.error(`✅ Upload concluído: ${fileUrl}`);

    return {
      success: true,
      fileId: fileId,
      fileName: fileName,
      url: fileUrl,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 🗂️ Criar pasta
async function createFolder(folderName, parentFolderId = null) {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    console.error(`🗂️ Criando pasta: "${folderName}"...`);

    const fileMetadata = {
      name: folderName,
      mimeType: "application/vnd.google-apps.folder",
    };

    if (parentFolderId) {
      fileMetadata.parents = [parentFolderId];
    }

    const folder = await drive.files.create({
      resource: fileMetadata,
      fields: "id, webViewLink",
    });

    const folderId = folder.data.id;
    const folderUrl = folder.data.webViewLink;

    console.error(`✅ Pasta criada: ${folderUrl}`);

    return {
      success: true,
      folderId: folderId,
      folderName: folderName,
      url: folderUrl,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 🔗 Compartilhar arquivo
async function shareFile(fileId, email, role = "editor") {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    await drive.permissions.create({
      fileId: fileId,
      requestBody: {
        role: role,
        type: "user",
        emailAddress: email,
      },
    });

    console.error(`✅ Arquivo compartilhado com ${email}`);

    return {
      success: true,
      message: `Arquivo compartilhado com ${email}`,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 🗑️ Deletar arquivo
async function deleteFile(fileId) {
  const auth = await getGoogleAuth();
  const drive = google.drive({ version: "v3", auth });

  try {
    await drive.files.delete({
      fileId: fileId,
    });

    console.error(`✅ Arquivo deletado`);

    return {
      success: true,
      message: "Arquivo deletado com sucesso",
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

module.exports = {
  listFiles,
  uploadFile,
  createFolder,
  shareFile,
  deleteFile,
};
