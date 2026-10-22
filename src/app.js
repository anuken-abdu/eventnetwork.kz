/* Event Network — скрипты сайта: меню, формы, фильтр, онлайн-ассистент */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var CFG = window.EN || {};
  var MQ = function (q) { return window.matchMedia(q).matches; };
  document.documentElement.classList.add("js");

  /* ---------- меню ---------- */
  var burger = $(".burger"), body = document.body;
  function setNav(o) { body.classList.toggle("nav-open", o); if (burger) burger.setAttribute("aria-expanded", o ? "true" : "false"); }
  if (burger) burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { setNav(false); closeChat(); } });
  window.addEventListener("resize", function () { if (!MQ("(max-width:1023px)")) setNav(false); });
  $$(".dd-t").forEach(function (b) {
    b.addEventListener("click", function () { var li = b.parentNode, o = li.classList.toggle("open"); b.setAttribute("aria-expanded", o ? "true" : "false"); });
  });
  $$(".f-col h4").forEach(function (h) { h.addEventListener("click", function () { if (MQ("(max-width:767px)")) h.parentNode.classList.toggle("open"); }); });

  /* ---------- наверх ---------- */
  var top = $(".totop"), tick = false;
  if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  window.addEventListener("scroll", function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { tick = false; if (top) top.hidden = window.pageYOffset < 700; });
  }, { passive: true });

  /* ---------- фильтр портфолио ---------- */
  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.getAttribute("data-f");
      $$(".chip").forEach(function (x) { var on = x === c; x.classList.toggle("on", on); x.setAttribute("aria-pressed", on ? "true" : "false"); });
      $$(".wk").forEach(function (w) { w.hidden = !(f === "all" || w.getAttribute("data-k") === f); });
    });
  });

  /* ---------- отправка заявок ---------- */
  function sendLead(data) {
    return fetch("/api/lead", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error("lead " + r.status); return r.json(); });
  }
  function mailto(data) {
    var lines = ["Имя: " + (data.name || "—"), "Контакт: " + data.contact, data.dir ? "Направление: " + data.dir : "", "", data.message || ""].filter(function (x, i) { return x || i > 2; });
    return "mailto:" + CFG.email + "?subject=" + encodeURIComponent("Заявка с сайта Event Network") + "&body=" + encodeURIComponent(lines.join("\n"));
  }
  var CONTACT_RE = /(\+?\d[\d\s()\-]{8,}\d)|([^\s@]+@[^\s@]+\.[^\s@]{2,})/;
  $$("form.frm").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = $(".frm-st", f), btn = $("button[type=submit]", f);
      var d = { name: f.name.value.trim(), contact: f.contact.value.trim(), dir: f.dir.value, message: f.message.value.trim(), page: location.pathname, source: "form" };
      var bad = false;
      [f.name, f.contact].forEach(function (i) { i.classList.remove("bad"); });
      if (!d.name) { f.name.classList.add("bad"); bad = true; }
      if (!CONTACT_RE.test(d.contact)) { f.contact.classList.add("bad"); bad = true; }
      if (!f.agree.checked) bad = true;
      st.className = "frm-st";
      if (bad) { st.classList.add("err"); st.textContent = !f.agree.checked ? "Отметьте согласие с политикой конфиденциальности." : "Укажите имя и телефон или электронную почту."; return; }
      btn.disabled = true; st.textContent = "Отправляем…";
      sendLead(d).then(function () {
        st.classList.add("ok"); st.textContent = "Спасибо! Заявка отправлена, мы свяжемся с вами в рабочее время.";
        f.reset(); f.agree.checked = true; track("lead_form");
      }).catch(function () {
        st.classList.add("ok");
        st.innerHTML = "Открываем почтовую программу с вашей заявкой. Если она не открылась, напишите нам на <a href=\"mailto:" + CFG.email + "\">" + CFG.email + "</a>.";
        location.href = mailto(d); track("lead_mailto");
      }).then(function () { btn.disabled = false; });
    });
  });
  function track(ev) { try { if (window.gtag) window.gtag("event", ev); } catch (e) {} }
  $$('a[href^="mailto:"]').forEach(function (a) { a.addEventListener("click", function () { track("email_click"); }); });
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener("click", function () { track("phone_click"); }); });

  /* ================= онлайн-ассистент ================= */
  var chat = $("#chat"), fab = $(".fab"), cb = $("#chatB"), cq = $("#chatQ"), cf = $("#chatF"), ci = $("#chatI");
  if (!chat) return;
  var hist = [], started = false, busy = false, apiOk = true, askedContact = false, leadSent = false;
  var DIRS = CFG.dirs || [];
  var dirLink = function (slug, name) { return "<a href=\"/napravleniya/" + slug + "/\">" + name + "</a>"; };
  var CONTACT_TXT = "Электронная почта: " + CFG.email + (CFG.phone ? "\nТелефон: " + CFG.phone : "") + "\nАдрес: " + CFG.addr + "\nВремя работы: " + CFG.hours;

  function openChat(q) {
    chat.hidden = false; body.classList.add("chat-open"); if (fab) fab.setAttribute("aria-expanded", "true");
    if (!started) { started = true; greet(); }
    if (q) setTimeout(function () { userSay(q); }, started ? 350 : 900);
    if (!MQ("(max-width:767px)")) setTimeout(function () { ci.focus(); }, 60);
    track("chat_open");
  }
  function closeChat() { if (!chat || chat.hidden) return; chat.hidden = true; body.classList.remove("chat-open"); if (fab) { fab.setAttribute("aria-expanded", "false"); fab.focus(); } }
  window.openChat = openChat;
  if (fab) fab.addEventListener("click", function () { openChat(); });
  $(".chat-x").addEventListener("click", closeChat);
  $$("[data-chat]").forEach(function (b) { b.addEventListener("click", function () { openChat("Расскажите подробнее о направлении «" + b.getAttribute("data-chat") + "»"); }); });

  function now() { var d = new Date(); return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function linkify(s) { return s.replace(/([\w.+-]+@[\w-]+\.[\w.]+)/g, "<a href=\"mailto:$1\">$1</a>").replace(/(^|[\s(«])(\/[a-z0-9\-\/]+\/)(?=[\s.,;:!?)»]|$)/g, "$1<a href=\"$2\">$2</a>"); }
  function add(role, htmlText) {
    var m = document.createElement("div"); m.className = "msg " + (role === "u" ? "msg-u" : "msg-b");
    m.innerHTML = htmlText + "<time>" + now() + "</time>"; cb.appendChild(m); cb.scrollTop = cb.scrollHeight; return m;
  }
  function typing() { var t = document.createElement("div"); t.className = "msg msg-b typing"; t.innerHTML = "<span></span><span></span><span></span>"; cb.appendChild(t); cb.scrollTop = cb.scrollHeight; return t; }
  function botSay(text, quick, isHtml) {
    var t = typing(), delay = Math.min(1600, 450 + text.length * 6);
    return new Promise(function (res) {
      setTimeout(function () { t.remove(); add("b", isHtml ? text : linkify(esc(text))); hist.push({ role: "assistant", content: text.replace(/<[^>]+>/g, "") }); setQuick(quick); res(); }, delay);
    });
  }
  function setQuick(list) {
    cq.innerHTML = "";
    (list || DEFAULT_Q).forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { userSay(q); }); cq.appendChild(b); });
  }
  var DEFAULT_Q = ["Какие у вас направления?", "Организовать мероприятие", "Сколько стоит?", "Как начать сотрудничество?", "Контакты"];
  function greet() {
    botSay("Здравствуйте! Я онлайн-ассистент Event Network. Расскажу о направлениях компании, форматах работы и помогу оставить заявку. Что вас интересует?");
  }
  function userSay(text) {
    text = String(text || "").trim(); if (!text || busy) return;
    add("u", esc(text)); hist.push({ role: "user", content: text }); cq.innerHTML = "";
    var m = text.match(CONTACT_RE);
    if (m && !leadSent) { captureLead(text, m[0]); return; }
    answer(text);
  }
  cf.addEventListener("submit", function (e) { e.preventDefault(); var v = ci.value; ci.value = ""; userSay(v); });

  function captureLead(text, contact) {
    leadSent = true; busy = true;
    var transcript = hist.map(function (h) { return (h.role === "user" ? "Клиент: " : "Ассистент: ") + h.content; }).join("\n").slice(-3000);
    sendLead({ name: "", contact: contact, message: transcript, page: location.pathname, source: "chat" }).then(function () {
      track("lead_chat");
      return botSay("Спасибо! Передал ваши контакты (" + contact + ") команде Event Network — с вами свяжутся в рабочее время, " + CFG.hours + ". Если хотите, опишите задачу подробнее здесь же.", ["Какие у вас направления?", "Как проходит работа?"]);
    }).catch(function () {
      leadSent = false;
      return botSay("Спасибо! Чтобы заявка точно дошла, отправьте её, пожалуйста, на почту " + CFG.email + " или через форму на странице контактов — там всё займёт минуту.", ["Открыть форму", "Контакты"]);
    }).then(function () { busy = false; });
  }

  function answer(text) {
    busy = true;
    var local = kb(text);
    // приветствия, контакты и форма — отвечаем сразу, остальное — через ИИ, если подключён
    if (local && local.instant) { return finish(local); }
    if (!apiOk) return finish(local || fallback());
    var t = typing();
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch("/api/chat", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-14), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) {
        clearTimeout(timer); t.remove();
        if (!j.reply) throw new Error("empty");
        add("b", linkify(esc(j.reply))); hist.push({ role: "assistant", content: j.reply });
        setQuick(local && local.quick); maybeAsk(); busy = false;
      })
      .catch(function () { clearTimeout(timer); t.remove(); apiOk = false; finish(local || fallback()); });
  }
  function finish(r) {
    botSay(r.text, r.quick, r.html).then(function () { if (r.after) r.after(); maybeAsk(); busy = false; });
  }
  function maybeAsk() {
    var userTurns = hist.filter(function (h) { return h.role === "user"; }).length;
    if (!askedContact && !leadSent && userTurns >= 3) {
      askedContact = true;
      var n = hist.length;
      setTimeout(function () { if (leadSent || busy || hist.length !== n) return; botSay("Если удобно, оставьте телефон или электронную почту прямо здесь — специалист свяжется и обсудит вашу задачу подробно."); }, 1500);
    }
  }
  function fallback() {
    return { text: "Хороший вопрос. Точный ответ зависит от задачи, поэтому лучше обсудить его со специалистом: оставьте здесь телефон или почту, либо напишите на " + CFG.email + ". А пока могу рассказать о направлениях и порядке работы.", quick: ["Какие у вас направления?", "Как проходит работа?", "Контакты"] };
  }

  /* ---------- база знаний (работает и без ИИ) ---------- */
  var D = {}; DIRS.forEach(function (d) { D[d[0]] = d; });
  var dl = function (slug) { var d = D[slug]; return d ? dirLink(d[0], d[1]) : ""; };
  var KB = [
    { k: ["привет", "здравств", "добрый", "салем", "сәлем", "hello", "hi "], instant: true, text: "Здравствуйте! Чем могу помочь? Могу рассказать о направлениях Event Network, порядке работы или помочь оставить заявку." },
    { k: ["спасибо", "рахмет", "благодар"], instant: true, text: "Пожалуйста! Если появятся вопросы — пишите, я на связи.", quick: ["Как начать сотрудничество?", "Контакты"] },
    { k: ["ты бот", "вы бот", "робот", "живой", "человек", "ии ", "нейросет"], instant: true, text: "Я онлайн-ассистент сайта, а не живой сотрудник. Отвечаю на общие вопросы о компании. Детали проекта, сроки и стоимость обсудит специалист — оставьте телефон или почту, и с вами свяжутся." },
    { k: ["контакт", "почт", "email", "e-mail", "телефон", "номер", "адрес", "где находит", "где вы", "связаться"], instant: true, text: "Контакты Event Network:\n" + CONTACT_TXT + "\n\nМожно оставить телефон или почту прямо здесь — передам специалисту.", quick: ["Открыть форму", "Как начать сотрудничество?"] },
    { k: ["открыть форму", "форма", "заявк", "оставить заявку"], instant: true, text: "Открываю форму заявки. Или просто напишите телефон или почту здесь — этого достаточно.", after: function () { location.href = "/kontakty/#form"; } },
    { k: ["направлен", "чем занимает", "что делает", "услуг", "что вы", "деятельност", "профил"], text: "Event Network — многопрофильная компания. Наши направления:\n• " + DIRS.map(function (d) { return dirLink(d[0], d[1]); }).join("\n• ") + "\n\nИх можно заказать отдельно или объединить в одном проекте.", html: true, quick: ["Организовать мероприятие", "Защита инфраструктуры", "Аналитика", "Коммуникации"] },
    { k: ["конференц", "форум", "мероприят", "ивент", "event", "выстав", "презентац", "деловая встреч", "деловые встреч", "семинар", "организовать"], text: "Готовим и проводим деловые мероприятия: конференции и форумы, деловые встречи, выставки и выставочные проекты, презентации. Можно заказать полную организацию или отдельные работы — например, программу или информационное сопровождение. Подробнее: " + dl("delovye-meropriyatiya-i-vystavki") + ".\n\nРасскажите о формате, дате и примерном числе участников — подскажу, с чего начать.", html: true, quick: ["За какой срок обращаться?", "Сколько стоит?", "Культурно-досуговые проекты"] },
    { k: ["досуг", "культур", "корпоратив", "праздник", "вечер", "тимбилд", "программ"], text: "Организуем культурно-досуговые проекты: тематические программы и вечера, досуговые мероприятия для коллективов и партнёров, форматы с вовлечением участников. Часто их совмещают с деловой частью. Подробнее: " + dl("kulturno-dosugovye-proekty") + ".", html: true, quick: ["Организовать мероприятие", "Сколько стоит?"] },
    { k: ["защит", "безопас", "киберб", "кибер", "инфраструкт", "уязвим", "взлом", "атак"], text: "Направление «" + (D["zashchita-cifrovoy-infrastruktury"] || [0, "Защита цифровой инфраструктуры"])[1] + "» — это работы по защите цифровых ресурсов, повышению информационной устойчивости и безопасности цифровой среды в рамках предоставляемых услуг. Состав работ определяем после знакомства с вашей цифровой средой и согласовываем заранее. Подробнее: " + dl("zashchita-cifrovoy-infrastruktury") + ".", html: true, quick: ["Конфиденциальность", "Как начать сотрудничество?"] },
    { k: ["конфиденц", "nda", "секрет", "тайн"], text: "Сведения о задачах и цифровой среде заказчика используются только для выполнения согласованных работ. Условия конфиденциальности можно закрепить в договоре." },
    { k: ["аналит", "мониторинг", "обзор", "исследован", "сбор информ", "сми", "информационное пространство"], text: "Информационно-аналитическая деятельность: мониторинг информационного пространства, сбор и систематизация сведений, анализ материалов, аналитические обзоры и справки по заданной теме. Мониторинг может быть разовым или регулярным. Подробнее: " + dl("informacionno-analiticheskaya-deyatelnost") + ".", html: true, quick: ["В каком виде результаты?", "Сколько стоит?"] },
    { k: ["в каком виде", "формат отчет", "отчёт", "отчет"], text: "Результаты передаём в виде аналитического обзора, справки или регулярного отчёта. Формат, периодичность и тематику согласовываем перед началом работы." },
    { k: ["маркетинг", "коммуникац", "pr", "пиар", "продвиж", "реклам", "аудитор", "smm"], text: "Маркетинговые и коммуникационные решения: информационное представление проектов, разработка коммуникационного подхода, подготовка материалов и поддержка взаимодействия с целевой аудиторией. Можно заказать для любого вашего проекта или мероприятия. Подробнее: " + dl("marketingovye-i-kommunikacionnye-resheniya") + ".", html: true, quick: ["Организовать мероприятие", "Сколько стоит?"] },
    { k: ["сайт", "веб", "платформ", "цифров", "информационн", "систем", "портал", "it"], text: "Цифровые технологии и информационные ресурсы: развитие и сопровождение сайтов и веб-платформ, работа с информационными системами, поддержка цифрового присутствия организации. Можно передать на сопровождение и уже существующий ресурс. Подробнее: " + dl("cifrovye-tehnologii") + ".", html: true, quick: ["Защита инфраструктуры", "Сколько стоит?"] },
    { k: ["вспомогат", "организационн", "координац", "дополнительн", "аутсорс"], text: "Вспомогательные коммерческие услуги — организационные и информационные задачи, которые сопровождают деловые процессы и проекты: поддержка проекта, координация, подготовка рабочих материалов. Их можно заказать отдельно или в составе проекта. Подробнее: " + dl("vspomogatelnye-kommercheskie-uslugi") + ".", html: true },
    { k: ["сколько стоит", "стоимост", "цена", "цены", "прайс", "бюджет", "тариф", "почем", "қанша"], text: "Стоимость рассчитывается индивидуально: она зависит от задачи, формата и объёма работ. Чтобы подготовить предложение, опишите проект — цель, формат, сроки — или оставьте телефон или почту, и специалист свяжется с вами.", quick: ["Как начать сотрудничество?", "Контакты"] },
    { k: ["срок", "когда", "заранее", "за какой", "быстро", "срочно"], text: "Сроки зависят от формата и масштаба. Для мероприятий чем раньше обращение, тем больше возможностей по площадке и программе. Точные сроки обсуждаем на первом созвоне — оставьте контакт, и специалист сориентирует.", quick: ["Как начать сотрудничество?", "Сколько стоит?"] },
    { k: ["как начать", "сотруднич", "работать с вами", "порядок", "как проходит", "этап", "процесс"], text: "Работаем так:\n1. Обсуждение задачи — цели, аудитория, сроки.\n2. Предложение — формат работы и состав задач.\n3. Подготовка и реализация — держим вас в курсе.\n4. Сопровождение — итоги, материалы и поддержка.\n\nЧтобы начать, оставьте телефон или почту здесь или заполните форму на сайте.", quick: ["Открыть форму", "Сколько стоит?"] },
    { k: ["договор", "документ", "безнал", "юрлиц", "юридическ", "счёт", "счет"], text: "Условия сотрудничества — состав работ и сроки — фиксируются в договоре. Детали оформления уточнит специалист при обсуждении проекта.", quick: ["Как начать сотрудничество?", "Контакты"] },
    { k: ["город", "астан", "шымкент", "регион", "казахстан", "алмат", "выезд"], text: "Компания находится в Алматы. Формат работы в других городах Казахстана обсуждается под конкретный проект — напишите, где и что планируете.", quick: ["Организовать мероприятие", "Контакты"] },
    { k: ["портфолио", "кейс", "пример", "работы", "проекты", "клиент", "отзыв"], text: "В разделе <a href=\"/portfolio/\">Портфолио</a> собраны направления работы компании. Примеры, подходящие под вашу задачу, специалист может показать при обсуждении проекта.", html: true, quick: ["Какие у вас направления?", "Как начать сотрудничество?"] },
    { k: ["график", "время работы", "часы", "выходн", "суббот"], text: "Время работы: " + CFG.hours + ". Сообщения в чате и заявки с сайта можно оставлять в любое время — их обработают в рабочие часы." },
    { k: ["комплекс", "несколько направлен", "вместе", "под ключ"], text: "Да, комплексный подход — основа нашей работы. Например, можно объединить организацию конференции, коммуникационное сопровождение и цифровые материалы в одном проекте с одной командой.", quick: ["Организовать мероприятие", "Как начать сотрудничество?"] },
    { k: ["язык", "казахск", "английск", "қазақ"], text: "На сайте информация на русском языке. Язык мероприятия, материалов и общения по проекту обсуждается с заказчиком." },
    { k: ["вакан", "работа у вас", "резюме", "трудоустр"], text: "По вопросам сотрудничества и вакансий напишите на " + CFG.email + " — письмо передадут ответственному сотруднику." },
    { k: ["как дела", "кто ты", "как тебя"], instant: true, text: "Всё хорошо, спасибо! Я онлайн-ассистент Event Network: подскажу по направлениям и помогу оставить заявку. Над каким проектом думаете?" },
  ];
  function kb(text) {
    var t = " " + text.toLowerCase().replace(/ё/g, "е") + " ", best = null, score = 0;
    KB.forEach(function (it) {
      var s = 0; it.k.forEach(function (k) { if (t.indexOf(k.replace(/ё/g, "е")) > -1) s += k.length; });
      if (s > score) { score = s; best = it; }
    });
    if (/^(открыть форму)$/i.test(text.trim())) return KB[4];
    return best;
  }
  // приветственная подсказка у кнопки через 25 секунд (один раз за визит)
  try {
    if (!sessionStorage.getItem("en_hint")) setTimeout(function () { if (!started && fab) { fab.classList.add("pulse"); sessionStorage.setItem("en_hint", "1"); } }, 25000);
  } catch (e) {}
})();
