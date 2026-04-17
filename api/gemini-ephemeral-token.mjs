// Mints a short-lived ephemeral token the browser can use to connect
// directly to the Gemini Live API (v1alpha). The real GEMINI_API_KEY
// never leaves the server.
//
// Docs: https://ai.google.dev/gemini-api/docs/ephemeral-tokens
// Model: https://ai.google.dev/gemini-api/docs/live

import { GoogleGenAI } from "@google/genai";

const MODEL_ID = "gemini-2.5-flash-native-audio-preview-12-2025";

export default async function handler(req, res) {
  // CORS — same-origin in prod, permissive for local testing
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();

  if (req.method !== "POST" && req.method !== "GET") {
    return res.status(405).json({ error: "method_not_allowed" });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "missing_GEMINI_API_KEY" });
  }

  try {
    const client = new GoogleGenAI({ apiKey });

    // 30 min total, 2 min window to start a new session
    const now = Date.now();
    const expireTime = new Date(now + 30 * 60 * 1000).toISOString();
    const newSessionExpireTime = new Date(now + 2 * 60 * 1000).toISOString();

    const token = await client.authTokens.create({
      config: {
        uses: 1,
        expireTime,
        newSessionExpireTime,
        httpOptions: { apiVersion: "v1alpha" },
      },
    });

    return res.status(200).json({
      token: token.name,
      model: MODEL_ID,
      expiresAt: expireTime,
    });
  } catch (err) {
    console.error("ephemeral-token error", err);
    return res.status(500).json({
      error: "token_mint_failed",
      message: String(err?.message || err),
    });
  }
}
