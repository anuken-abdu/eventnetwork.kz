// Vercel Function: приём заявок с сайта и из чата.
// Доставка в Telegram: переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID (Vercel → Settings → Environment Variables).
// Если они не заданы, функция отвечает 503, а сайт открывает письмо с заявкой на почту компании.
const hits = new Map();
function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
  arr.push(now); hits.set(ip, arr); if (hits.size > 5000) hits.clear();
  return arr.length > 8;
}
const clip = (v, n) => (typeof v === "string" ? v.trim().slice(0, n) : "");

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const token = process.env.TELEGRAM_BOT_TOKEN, chat = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }
  let b = req.body; if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  const contact = clip(b && b.contact, 120);
  if (!/(\+?\d[\d\s()\-]{8,}\d)|([^\s@]+@[^\s@]+\.[^\s@]{2,})/.test(contact)) { res.status(400).json({ error: "contact" }); return; }
  const lines = [
    b.source === "chat" ? "💬 Заявка из чата eventnetwork.kz" : "📩 Заявка с сайта eventnetwork.kz",
    clip(b.name, 80) && "Имя: " + clip(b.name, 80),
    "Контакт: " + contact,
    clip(b.dir, 120) && "Направление: " + clip(b.dir, 120),
    clip(b.page, 120) && "Страница: " + clip(b.page, 120),
    clip(b.message, 3000) && "\n" + clip(b.message, 3000),
  ].filter(Boolean);
  try {
    const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ chat_id: chat, text: lines.join("\n").slice(0, 4000), disable_web_page_preview: true }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    res.status(200).json({ ok: true });
  } catch (e) { res.status(502).json({ error: "fail" }); }
};
