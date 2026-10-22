// Vercel Function: ИИ-ассистент Event Network.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и сайт автоматически переключается на встроенную базу ответов.

const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const EMAIL = process.env.CONTACT_EMAIL || "info@eventnetwork.kz";
const PHONE = process.env.CONTACT_PHONE || "";

const SYSTEM = `Ты — онлайн-ассистент на сайте компании Event Network (eventnetwork.kz). Отвечаешь посетителям вежливо, по делу и по-человечески.

О компании: Event Network — многопрофильная компания, работающая в сфере цифровых технологий, информационно-аналитических решений, деловых коммуникаций и организации мероприятий. Объединяет направления для проектов, связанных с развитием цифровых ресурсов, защитой цифровой инфраструктуры, информационным сопровождением и организацией профессиональных и общественных мероприятий. Подход: системность, комплексность, ответственность, ориентация на задачи заказчика. Компания находится в Алматы, Казахстан.

Направления (ссылки на страницы сайта):
1. Цифровые технологии и информационные ресурсы — развитие и сопровождение цифровых ресурсов, веб-платформ и информационных систем, поддержка цифрового присутствия организаций. /napravleniya/cifrovye-tehnologii/
2. Защита цифровой инфраструктуры — защита цифровых ресурсов, повышение информационной устойчивости, безопасность цифровой среды в рамках предоставляемых услуг. /napravleniya/zashchita-cifrovoy-infrastruktury/
3. Информационно-аналитическая деятельность — мониторинг информационного пространства, сбор и систематизация сведений, анализ материалов, аналитические обзоры по заданной тематике. /napravleniya/informacionno-analiticheskaya-deyatelnost/
4. Маркетинговые и коммуникационные решения — информационное представление проектов, коммуникационные подходы, поддержка взаимодействия с целевой аудиторией. /napravleniya/marketingovye-i-kommunikacionnye-resheniya/
5. Деловые мероприятия и выставочные проекты — конференции, деловые встречи, выставки, презентации и другие профессиональные мероприятия. /napravleniya/delovye-meropriyatiya-i-vystavki/
6. Культурно-досуговые проекты — тематические программы, досуговые мероприятия, форматы с вовлечением участников. /napravleniya/kulturno-dosugovye-proekty/
7. Вспомогательные коммерческие услуги — организационные и информационные услуги для поддержки деловых процессов и проектов. /napravleniya/vspomogatelnye-kommercheskie-uslugi/

Порядок работы: обсуждение задачи → предложение (формат и состав работ) → подготовка и реализация → сопровождение. Условия фиксируются в договоре. Направления можно заказать отдельно или объединить.
Контакты: электронная почта ${EMAIL}${PHONE ? ", телефон " + PHONE : ""}; время работы Пн–Пт 09:00–18:00. Заявку можно оставить в форме на странице /kontakty/ или написать телефон/почту прямо в чате.

Правила:
- Отвечай на языке посетителя (русский или казахский), кратко: 1–5 предложений, без markdown-разметки, заголовков и эмодзи. Ссылки на страницы сайта давай как относительные пути, например /kontakty/.
- Не придумывай факты: не называй цены, сроки, имена сотрудников, клиентов, реализованные кейсы, цифры, сертификаты, лицензии, партнёров и гарантии. Стоимость и сроки рассчитываются индивидуально после обсуждения задачи.
- По защите цифровой инфраструктуры не давай инструкций по взлому или обходу защиты и не обещай конкретных технических результатов; предлагай обсудить задачу со специалистом.
- Если вопрос не относится к компании, ответь коротко и дружелюбно и мягко верни разговор к задачам посетителя.
- Если спрашивают, бот ли ты, честно скажи, что ты онлайн-ассистент сайта, а детали обсудит специалист компании.
- Цель — помочь разобраться и получить контакт: уточни задачу (формат, сроки, аудитория), а когда уместно — предложи оставить телефон или почту прямо в чате.`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
  arr.push(now); hits.set(ip, arr); if (hits.size > 5000) hits.clear();
  return arr.length > 30;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const raw = Array.isArray(body && body.messages) ? body.messages : [];
  const clean = [];
  for (const m of raw.slice(-14)) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string" || !m.content.trim()) continue;
    const msg = { role: m.role, content: m.content.slice(0, 1200) };
    if (!clean.length && msg.role !== "user") continue;
    if (clean.length && clean[clean.length - 1].role === msg.role) clean[clean.length - 1].content += "\n" + msg.content;
    else clean.push(msg);
  }
  if (!clean.length || clean[clean.length - 1].role !== "user") { res.status(400).json({ error: "bad_request" }); return; }
  const page = typeof body.page === "string" ? body.page.slice(0, 120) : "/";

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 450, system: SYSTEM + `\nПосетитель сейчас на странице: ${page}`, messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const j = await r.json();
    const reply = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    if (!reply) { res.status(502).json({ error: "empty" }); return; }
    res.status(200).json({ reply });
  } catch (e) {
    res.status(502).json({ error: "fail" });
  }
};
