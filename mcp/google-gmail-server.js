#!/usr/bin/env node

/**
 * MCP Server para Gmail
 * Enviar emails, ler mensagens, gerenciar labels
 */

const { google } = require("googleapis");
const fs = require("fs");
const path = require("path");

const CREDENTIALS_FILE = path.join(
  process.env.HOME,
  "Downloads",
  "thiagodias-30c5309274a4.json"
);

const SCOPES = ["https://www.googleapis.com/auth/gmail.modify"];

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

// 📨 Enviar email
async function sendEmail(to, subject, body, cc = null, bcc = null) {
  const auth = await getGoogleAuth();
  const gmail = google.gmail({ version: "v1", auth });

  try {
    console.error(`📨 Enviando email para ${to}...`);

    // Construir headers do email
    let emailContent = `To: ${to}\r\n`;
    emailContent += `Subject: ${subject}\r\n`;

    if (cc) {
      emailContent += `Cc: ${cc}\r\n`;
    }
    if (bcc) {
      emailContent += `Bcc: ${bcc}\r\n`;
    }

    emailContent += `\r\n${body}`;

    // Encodar em base64
    const encodedMessage = Buffer.from(emailContent)
      .toString("base64")
      .replace(/\+/g, "-")
      .replace(/\//g, "_");

    const result = await gmail.users.messages.send({
      userId: "me",
      requestBody: {
        raw: encodedMessage,
      },
    });

    console.error(`✅ Email enviado com sucesso (ID: ${result.data.id})`);

    return {
      success: true,
      messageId: result.data.id,
      to: to,
      subject: subject,
      message: "Email enviado com sucesso",
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 📧 Listar emails
async function listEmails(query = "is:unread", limit = 10) {
  const auth = await getGoogleAuth();
  const gmail = google.gmail({ version: "v1", auth });

  try {
    const result = await gmail.users.messages.list({
      userId: "me",
      q: query,
      maxResults: limit,
    });

    if (!result.data.messages) {
      return {
        success: true,
        messages: [],
        message: "Nenhum email encontrado",
      };
    }

    const messages = [];

    for (const msg of result.data.messages) {
      const fullMessage = await gmail.users.messages.get({
        userId: "me",
        id: msg.id,
        format: "metadata",
        metadataHeaders: ["Subject", "From", "To", "Date"],
      });

      const headers = fullMessage.data.payload.headers;
      const subject = headers.find((h) => h.name === "Subject")?.value || "";
      const from = headers.find((h) => h.name === "From")?.value || "";
      const date = headers.find((h) => h.name === "Date")?.value || "";

      messages.push({
        id: msg.id,
        subject: subject,
        from: from,
        date: date,
      });
    }

    return {
      success: true,
      messages: messages,
      count: messages.length,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 📖 Ler email
async function readEmail(messageId) {
  const auth = await getGoogleAuth();
  const gmail = google.gmail({ version: "v1", auth });

  try {
    const message = await gmail.users.messages.get({
      userId: "me",
      id: messageId,
      format: "full",
    });

    const headers = message.data.payload.headers;
    const subject = headers.find((h) => h.name === "Subject")?.value || "";
    const from = headers.find((h) => h.name === "From")?.value || "";
    const to = headers.find((h) => h.name === "To")?.value || "";
    const date = headers.find((h) => h.name === "Date")?.value || "";

    // Extrair corpo do email
    let body = "";
    if (message.data.payload.parts) {
      for (const part of message.data.payload.parts) {
        if (part.mimeType === "text/plain" && part.body.data) {
          body = Buffer.from(part.body.data, "base64").toString("utf-8");
          break;
        }
      }
    } else if (message.data.payload.body.data) {
      body = Buffer.from(message.data.payload.body.data, "base64").toString(
        "utf-8"
      );
    }

    return {
      success: true,
      messageId: messageId,
      subject: subject,
      from: from,
      to: to,
      date: date,
      body: body,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

// 🏷️ Adicionar label
async function addLabel(messageId, labelName) {
  const auth = await getGoogleAuth();
  const gmail = google.gmail({ version: "v1", auth });

  try {
    // Obter labels
    const labelsResult = await gmail.users.labels.list({
      userId: "me",
    });

    const label = labelsResult.data.labels.find((l) => l.name === labelName);

    if (!label) {
      throw new Error(`Label "${labelName}" não encontrado`);
    }

    await gmail.users.messages.modify({
      userId: "me",
      id: messageId,
      requestBody: {
        addLabelIds: [label.id],
      },
    });

    console.error(`✅ Label "${labelName}" adicionado`);

    return {
      success: true,
      message: `Label "${labelName}" adicionado ao email`,
    };
  } catch (error) {
    console.error(`❌ Erro: ${error.message}`);
    throw error;
  }
}

module.exports = {
  sendEmail,
  listEmails,
  readEmail,
  addLabel,
};
