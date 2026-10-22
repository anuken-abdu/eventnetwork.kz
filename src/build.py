# -*- coding: utf-8 -*-
"""Статический генератор сайта Event Network: python3 src/build.py → dist/"""
import html, json, pathlib, shutil, datetime
from data import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "2610222359"
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)

# ---------- иконки (линейные, 24×24) ----------
P = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "megaphone": '<path d="M3 10v4a1 1 0 0 0 1 1h3l6 4V5L7 9H4a1 1 0 0 0-1 1z"/><path d="M17 8.5a5 5 0 0 1 0 7M19.5 6a8.5 8.5 0 0 1 0 12"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8 14h2M14 14h2M8 17h2"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "send": '<path d="M4 12l16-8-6 16-3-7z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a5.5 5.5 0 0 1 3.5 6"/>',
    "wa": '<path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.4-4.3a8.5 8.5 0 1 1 15.6-4.5z"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .5.4l.7 1.6c0 .2 0 .4-.1.5l-.5.6c-.1.2-.1.3 0 .5.5.9 1.3 1.7 2.3 2.2.2.1.3.1.5-.1l.6-.7c.1-.2.3-.2.5-.1l1.6.8c.2.1.3.2.3.3 0 .7-.4 1.4-1 1.6-.7.3-1.6.3-3.4-.6a8.8 8.8 0 0 1-3.2-3.1c-.7-1.2-.8-2.2-.1-3.6z"/>',
}
def ic(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{P[name]}</g></svg>'

LOGO_MARK = '''<svg class="logo-m" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="#c9a35c" stroke-width="1.6"><circle cx="24" cy="24" r="19"/><ellipse cx="24" cy="24" rx="8.5" ry="19"/><path d="M5.5 18h37M5.5 30h37"/></g><g fill="#c9a35c"><circle cx="24" cy="5" r="2.6"/><circle cx="5.6" cy="18" r="2.2"/><circle cx="42.4" cy="30" r="2.2"/><circle cx="15.5" cy="30" r="2"/><circle cx="32.5" cy="18" r="2"/><circle cx="24" cy="43" r="2.6"/></g></svg>'''
def logo(dark=False):
    return f'<a class="logo{" logo-d" if dark else ""}" href="/" aria-label="{BRAND} — на главную">{LOGO_MARK}<span><b>EVENT</b><b>NETWORK</b></span></a>'


# Баннеры для превью ссылок (1200×630): url → (файл, заголовок, строка под ним, фон)
OG = {
    "/": ("home", HERO_H1, "Цифровая среда · коммуникации · мероприятия", "hero"),
    "/o-kompanii/": ("o-kompanii", "О компании Event Network", "Многопрофильные решения для современных задач", "about"),
    "/napravleniya/": ("napravleniya", "Направления деятельности", "Комплексные решения в различных направлениях", "portfolio"),
    "/portfolio/": ("portfolio", "Портфолио", "Направления работы и компетенции компании", "portfolio"),
    "/kontakty/": ("kontakty", "Открыты к деловому сотрудничеству", "Обсудим задачи и формат взаимодействия", "contacts"),
    "/politika-konfidencialnosti/": ("politika", "Политика конфиденциальности", "Обработка и защита персональных данных", "quote"),
}
for _d in DIRS:
    OG[f'/napravleniya/{_d["slug"]}/'] = (_d["slug"], _d["name"], "Направление Event Network", _d["img"])

def dir_by(slug): return next(d for d in DIRS if d["slug"] == slug)
def img(name, alt, cls="", w=960, h=640, lazy=True):
    return f'<img class="{cls}" src="/assets/img/{name}.webp?v={VER}" alt="{E(alt)}" width="{w}" height="{h}"{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}>'

NAV = [("/", "Главная"), ("/o-kompanii/", "О компании"), ("/napravleniya/", "Направления"), ("/portfolio/", "Портфолио"), ("/kontakty/", "Контакты")]

def header(cur):
    items = ""
    for href, name in NAV:
        a = ' aria-current="page"' if cur == href else ""
        if href == "/napravleniya/":
            sub = "".join(f'<a href="/napravleniya/{d["slug"]}/">{ic(d["icon"])}<span>{d["name"]}</span></a>' for d in DIRS)
            items += f'<li class="has-dd"><a href="{href}"{a}>{name}</a><button class="dd-t" type="button" aria-label="Открыть список направлений" aria-expanded="false">{ic("chev")}</button><div class="dd">{sub}</div></li>'
        else:
            items += f'<li><a href="{href}"{a}>{name}</a></li>'
    contact = f'<a class="hdr-c" href="tel:{PHONE.replace(" ", "")}">{ic("phone")}<span>{PHONE}</span></a>' if PHONE else f'<a class="hdr-c" href="mailto:{EMAIL}">{ic("mail")}<span>{EMAIL}</span></a>'
    return f'''<a class="skip" href="#main">Перейти к содержанию</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}
<nav class="nav" id="nav" aria-label="Основное меню"><ul>{items}</ul>
<div class="nav-m">{contact}<a class="btn btn-g" href="/kontakty/#form">Связаться с нами</a></div></nav>
<div class="hdr-r">{contact}<a class="btn btn-g btn-s" href="/kontakty/#form">Связаться</a>
<button class="burger" type="button" aria-label="Меню" aria-controls="nav" aria-expanded="false">{ic("menu", "i i-o")}{ic("close", "i i-c")}</button></div></div></header>'''

def footer():
    dirs = "".join(f'<li><a href="/napravleniya/{d["slug"]}/">{d["name"]}</a></li>' for d in DIRS)
    pages = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in NAV)
    ct = ""
    if PHONE: ct += f'<li><a href="tel:{PHONE.replace(" ", "")}">{ic("phone")}{PHONE}</a></li>'
    ct += f'<li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("pin")}{ADDRESS}</li><li>{ic("clock")}{HOURS}</li>'
    y = datetime.date.today().year
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-g"><div class="ftr-a">{logo(True)}<p>Многопрофильная компания: цифровые технологии, защита цифровой инфраструктуры, аналитика, коммуникации и организация мероприятий.</p><a class="btn btn-g btn-s" href="/kontakty/#form">Обсудить проект</a></div>
<div class="f-col"><h4>Разделы {ic("chev")}</h4><ul>{pages}</ul></div>
<div class="f-col f-wide"><h4>Направления {ic("chev")}</h4><ul>{dirs}</ul></div>
<div class="f-col f-ct"><h4>Контакты {ic("chev")}</h4><ul>{ct}</ul></div></div>
<div class="ftr-b"><span>© {y} {BRAND}</span><a href="/politika-konfidencialnosti/">Политика конфиденциальности</a><a href="{DEV_URL}" target="_blank" rel="noopener">Разработка сайта — {DEV_NAME}</a></div>
</div></footer>
<button class="totop" type="button" aria-label="Наверх" hidden>{ic("up")}</button>
<button class="fab" type="button" aria-controls="chat" aria-expanded="false"><span class="fab-d"></span>{ic("chat")}<span class="fab-t">Задать вопрос</span></button>
<section class="chat" id="chat" role="dialog" aria-label="Онлайн-ассистент Event Network" hidden>
<div class="chat-h">{LOGO_MARK}<div><b>Ассистент Event Network</b><small><i></i>Онлайн · отвечает сразу</small></div><button class="chat-x" type="button" aria-label="Закрыть чат">{ic("close")}</button></div>
<div class="chat-b" id="chatB" aria-live="polite"></div>
<div class="chat-q" id="chatQ"></div>
<form class="chat-f" id="chatF" autocomplete="off"><label class="sr" for="chatI">Ваш вопрос</label><input id="chatI" type="text" maxlength="600" placeholder="Напишите вопрос…"><button type="submit" aria-label="Отправить">{ic("send")}</button></form>
</section>'''

def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{n}</a></li>' if h else f'<li aria-current="page">{n}</li>' for h, n in items)
    return f'<nav class="crumbs" aria-label="Хлебные крошки"><ol>{lis}</ol></nav>'

def ld_crumbs(items, url):
    el = [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h or url)} for i, (h, n) in enumerate(items)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}

def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
       "logo": SITE + "/icon-512.png", "email": EMAIL, "description": INTRO[0],
       "address": {"@type": "PostalAddress", "addressLocality": "Алматы", "addressCountry": "KZ"},
       "areaServed": {"@type": "Country", "name": "Казахстан"},
       "knowsAbout": [d["name"] for d in DIRS],
       "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "email": EMAIL, "availableLanguage": ["ru"], **({"telephone": PHONE} if PHONE else {})}]}
if PHONE: ORG["telephone"] = PHONE

def page(url, title, desc, body, cur="", ld=None, og=None):
    og = og or ("og/" + OG[url][0] if url in OG else "og")
    full = SITE + url
    lds = [ORG] + (ld or [])
    if url == "/":
        lds.append({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/", "inLanguage": "ru"})
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    ga = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>''' if GA_ID else ""
    gsc = f'<meta name="google-site-verification" content="{GSC_META}">' if GSC_META else ""
    cfg = json.dumps({"email": EMAIL, "phone": PHONE, "wa": WHATSAPP, "hours": HOURS, "addr": ADDRESS, "dirs": [[d["slug"], d["name"], d["short"]] for d in DIRS]}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{full}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b1b33">{gsc}
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{full}">
<meta property="og:image" content="{SITE}/assets/img/{og}.jpg?v={VER}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{E(title)}"><meta name="twitter:image" content="{SITE}/assets/img/{og}.jpg?v={VER}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/manrope-cyrillic-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/onest-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{ld_html}{ga}
</head><body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
<script>window.EN={cfg};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''

def write(url, content):
    p = DIST / url.strip("/") / "index.html" if url != "/" else DIST / "index.html"
    if url == "/404/": p = DIST / "404.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

# ---------- общие блоки ----------
def sec_h(title, sub="", link=None, cls=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ic("arrow")}</a>' if link else ""
    s = f'<p>{sub}</p>' if sub else ""
    return f'<div class="sec-h {cls}"><div><h2>{title}</h2>{s}</div>{lk}</div>'

def dir_cards(exclude=None):
    out = ""
    for d in DIRS:
        if d["slug"] == exclude: continue
        out += f'''<a class="dc" href="/napravleniya/{d["slug"]}/"><span class="dc-im">{img(d["img"], d["name"])}</span>
<span class="dc-b"><span class="dc-i">{ic(d["icon"])}</span><b>{d["name"]}</b><span class="dc-t">{d["text"]}</span><span class="more">Подробнее {ic("arrow")}</span></span></a>'''
    return f'<div class="dc-g">{out}</div>'

def principles():
    return '<div class="pr-g">' + "".join(f'<div class="pr"><span class="pr-i">{ic(i)}</span><b>{t}</b><p>{d}</p></div>' for i, t, d in PRINCIPLES) + "</div>"

def steps():
    return '<ol class="st">' + "".join(f'<li><span class="st-n">{i+1:02d}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS)) + "</ol>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{q}{ic("chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faq) + "</div>"

def quote_band():
    return f'''<section class="qb"><div class="qb-bg">{img("quote", "", w=1800, h=560)}</div><div class="wrap qb-in"><p>«{QUOTE}»</p><a class="btn btn-g" href="/kontakty/#form">Связаться с нами {ic("arrow")}</a></div></section>'''

def form_html(fid="form", title="Напишите нам", sub="Опишите задачу — свяжемся, чтобы обсудить формат и детали."):
    opts = "".join(f'<option>{d["name"]}</option>' for d in DIRS)
    return f'''<form class="frm" id="{fid}" novalidate>
<h3>{title}</h3><p class="frm-s">{sub}</p>
<div class="fld"><label for="{fid}-n">Ваше имя</label><input id="{fid}-n" name="name" type="text" autocomplete="name" required maxlength="80"></div>
<div class="fld"><label for="{fid}-c">Телефон или электронная почта</label><input id="{fid}-c" name="contact" type="text" autocomplete="email" required maxlength="120"></div>
<div class="fld"><label for="{fid}-d">Направление</label><select id="{fid}-d" name="dir"><option value="">Не выбрано</option>{opts}</select></div>
<div class="fld"><label for="{fid}-m">Сообщение</label><textarea id="{fid}-m" name="message" rows="4" maxlength="2000"></textarea></div>
<label class="chk"><input type="checkbox" name="agree" required checked><span>Согласен с <a href="/politika-konfidencialnosti/">политикой конфиденциальности</a></span></label>
<button class="btn btn-g btn-w" type="submit">Отправить {ic("send")}</button>
<p class="frm-st" role="status" aria-live="polite"></p>
</form>'''

def contact_list():
    li = ""
    if PHONE: li += f'<li><span class="ci">{ic("phone")}</span><div><small>Телефон</small><a href="tel:{PHONE.replace(" ", "")}">{PHONE}</a></div></li>'
    li += f'<li><span class="ci">{ic("mail")}</span><div><small>Электронная почта</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>'
    li += f'<li><span class="ci">{ic("pin")}</span><div><small>Адрес</small><span>{ADDRESS}</span></div></li>'
    li += f'<li><span class="ci">{ic("clock")}</span><div><small>Время работы</small><span>{HOURS}</span></div></li>'
    return f'<ul class="cl">{li}</ul>'

def cta_sec():
    return f'''<section class="sec sec-alt"><div class="wrap cta">
<div class="cta-t"><span class="eyebrow">Сотрудничество</span><h2>Открыты к деловому сотрудничеству</h2><p>Если вы заинтересованы в сотрудничестве с Event Network, свяжитесь с нами для обсуждения задач, формата взаимодействия и возможных направлений совместной работы.</p>{contact_list()}</div>
{form_html("form", "Обсудим ваш проект")}</div></section>'''

def banner(title, sub, image, items):
    return f'''<section class="pb"><div class="pb-bg">{img(image, "", w=1800, h=600, lazy=False)}</div><div class="wrap pb-in">{crumbs(items)}<h1>{title}</h1><p>{sub}</p></div></section>'''

# ---------- страницы ----------
def build_home():
    strip = "".join(f'<a class="hs" href="/napravleniya/{s}/">{ic(i)}<span>{t}</span></a>' for i, t, s in HOME_DIRS)
    body = f'''<section class="hero"><div class="hero-bg">{img("hero", "", w=2000, h=1000, lazy=False)}</div>
<div class="wrap hero-in"><span class="eyebrow eyebrow-l">Многопрофильная компания · Казахстан</span><h1>{HERO_H1}</h1><p class="hero-s">{HERO_SUB}</p>
<div class="btns"><a class="btn btn-g" href="/napravleniya/">Наши направления {ic("arrow")}</a><a class="btn btn-ol" href="/kontakty/#form">Связаться с нами</a></div></div></section>
<section class="hstrip" aria-label="Основные направления"><div class="wrap"><div class="hs-g">{strip}</div></div></section>
<section class="sec"><div class="wrap split">
<div class="split-im">{img("events", "Деловое мероприятие: сцена и участники")}</div>
<div><span class="eyebrow">О компании</span><h2>Event Network — ваш партнёр в реализации идей и проектов</h2>{"".join(f"<p>{t}</p>" for t in INTRO)}
<div class="btns"><a class="btn btn-n" href="/o-kompanii/">О компании {ic("arrow")}</a></div></div></div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Основные направления", "Семь направлений деятельности, которые можно заказать отдельно или объединить в одном проекте.", ("Все направления", "/napravleniya/"))}{dir_cards()}</div></section>
<section class="sec"><div class="wrap">{sec_h("Комплексный подход", COMPLEX)}{principles()}</div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Как мы работаем", "Последовательный порядок взаимодействия от первого обсуждения до сопровождения.")}{steps()}</div></section>
{quote_band()}
<section class="sec"><div class="wrap faq-w">{sec_h("Частые вопросы", "Не нашли ответа — спросите онлайн-ассистента или напишите нам.")}{faq_html(FAQ_HOME)}</div></section>
{cta_sec()}'''
    write("/", page("/", f"{BRAND} — цифровые технологии, аналитика и организация мероприятий", "Event Network — многопрофильная компания в Казахстане: цифровые ресурсы, защита цифровой инфраструктуры, информационная аналитика, коммуникационные решения, деловые и культурно-досуговые мероприятия.", body, "/", [ld_faq(FAQ_HOME)]))

def build_about():
    it = [("/", "Главная"), (None, "О компании")]
    body = f'''{banner("О компании", "Многопрофильные решения для современных задач", "about", it)}
<section class="sec"><div class="wrap ab">
<div class="ab-t"><span class="eyebrow">Event Network — многопрофильная компания</span>{"".join(f"<p>{t}</p>" for t in ABOUT)}</div>
<aside class="ab-n">{ic("star")}<p>Наш подход — системность, внимание к задачам заказчика и комплексное рассмотрение каждого проекта.</p></aside></div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Наш подход", "Принципы, на которых строится работа над каждым проектом.")}{principles()}</div></section>
<section class="sec"><div class="wrap">{sec_h("Направления деятельности", "", ("Все направления", "/napravleniya/"))}
<ul class="dl">{"".join(f'<li><a href="/napravleniya/{d["slug"]}/">{ic(d["icon"])}<span><b>{d["name"]}</b><small>{d["text"]}</small></span>{ic("arrow", "i dl-a")}</a></li>' for d in DIRS)}</ul></div></section>
{quote_band()}{cta_sec()}'''
    write("/o-kompanii/", page("/o-kompanii/", f"О компании {BRAND} — многопрофильные решения для современных задач", "Event Network объединяет цифровые технологии, защиту цифровой инфраструктуры, информационную аналитику, коммуникации и организацию мероприятий. Наш подход: системность, комплексность, ответственность.", body, "/o-kompanii/", [ld_crumbs(it, "/o-kompanii/")]))

def build_dirs():
    it = [("/", "Главная"), (None, "Направления")]
    body = f'''{banner("Наши направления", "Комплексные решения в различных направлениях", "portfolio", it)}
<section class="sec"><div class="wrap">{dir_cards()}</div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Комплексный подход", COMPLEX)}{steps()}</div></section>{cta_sec()}'''
    ld = [ld_crumbs(it, "/napravleniya/"), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}/napravleniya/{d["slug"]}/', "name": d["name"]} for i, d in enumerate(DIRS)]}]
    write("/napravleniya/", page("/napravleniya/", f"Услуги и направления деятельности — {BRAND}", "Цифровые технологии, защита цифровой инфраструктуры, информационно-аналитическая деятельность, маркетинг и коммуникации, деловые и выставочные мероприятия, культурно-досуговые проекты, вспомогательные услуги.", body, "/napravleniya/", ld))
    for d in DIRS:
        url = f'/napravleniya/{d["slug"]}/'
        it2 = [("/", "Главная"), ("/napravleniya/", "Направления"), (None, d["name"])]
        items = "".join(f'<li>{ic("check")}<span>{x}</span></li>' for x in d["items"])
        body = f'''{banner(d["name"], d["text"], d["img"], it2)}
<section class="sec"><div class="wrap dt-g">
<div class="dt-t"><span class="eyebrow">О направлении</span><h2>{d["lead"]}</h2>
<h3>Что входит</h3><ul class="ck">{items}</ul>
<div class="who">{ic("users")}<div><b>Кому подходит</b><p>{d["who"]}</p></div></div></div>
<aside class="dt-side"><div class="dt-im">{img(d["img"], d["name"])}</div><div class="dt-box"><b>Обсудим вашу задачу</b><p>Стоимость и сроки рассчитываем индивидуально после обсуждения проекта.</p><a class="btn btn-g btn-w" href="#form">Оставить заявку</a><button class="btn btn-ol2 btn-w" type="button" data-chat="{E(d["short"])}">Спросить ассистента</button></div></aside></div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Как мы работаем")}{steps()}</div></section>
<section class="sec"><div class="wrap faq-w">{sec_h("Вопросы по направлению")}{faq_html(d["faq"])}</div></section>
<section class="sec sec-alt"><div class="wrap">{sec_h("Другие направления", "", ("Все направления", "/napravleniya/"))}{dir_cards(exclude=d["slug"])}</div></section>{cta_sec()}'''
        svc = {"@context": "https://schema.org", "@type": "Service", "name": d["name"], "description": d["text"], "serviceType": d["name"], "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "Country", "name": "Казахстан"}, "url": SITE + url}
        write(url, page(url, f'{d["name"]} — {BRAND}', f'{d["text"]} Event Network, Казахстан.'[:300], body, "/napravleniya/", [svc, ld_crumbs(it2, url), ld_faq(d["faq"])]))

def build_portfolio():
    it = [("/", "Главная"), (None, "Портфолио")]
    chips = "".join(f'<button type="button" class="chip{" on" if k == "all" else ""}" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in WORK_FILTERS)
    cards = "".join(f'''<article class="wk" data-k="{k}"><div class="wk-im">{img(im, t)}</div><div class="wk-b"><b>{t}</b><p>{d}</p><a class="more" href="/napravleniya/{s}/">О направлении {ic("arrow")}</a></div></article>''' for im, k, t, d, s in WORKS)
    body = f'''{banner("Портфолио", "Направления работы и компетенции компании", "portfolio", it)}
<section class="sec"><div class="wrap">{sec_h("Направления работы", "Основные типы проектов, которые выполняет Event Network. Подробности о составе работ — на страницах направлений.")}
<div class="chips" role="group" aria-label="Фильтр по направлениям">{chips}</div><div class="wk-g">{cards}</div></div></section>
<section class="sec sec-alt"><div class="wrap split split-r"><div><span class="eyebrow">Ваш проект</span><h2>Расскажите о задаче — предложим формат работы</h2><p>Опишите цели проекта, аудиторию и желаемые сроки. Мы рассмотрим задачу комплексно и предложим подходящее сочетание направлений.</p><div class="btns"><a class="btn btn-g" href="#form">Обсудить проект {ic("arrow")}</a></div></div><div class="split-im">{img("marketing", "Коммуникационные решения")}</div></div></section>{cta_sec()}'''
    write("/portfolio/", page("/portfolio/", f"Портфолио и направления работы — {BRAND}", "Цифровые и информационные проекты, аналитические задачи, коммуникационные проекты, деловые и выставочные мероприятия, культурно-досуговые инициативы Event Network.", body, "/portfolio/", [ld_crumbs(it, "/portfolio/")]))

def build_contacts():
    it = [("/", "Главная"), (None, "Контакты")]
    body = f'''{banner("Контакты", "Открыты к деловому сотрудничеству", "contacts", it)}
<section class="sec"><div class="wrap cta">
<div class="cta-t"><h2>Свяжитесь с нами</h2><p>Если вы заинтересованы в сотрудничестве с Event Network, свяжитесь с нами для обсуждения задач, формата взаимодействия и возможных направлений совместной работы.</p>{contact_list()}
<p class="final">Мы открыты к профессиональному взаимодействию и рассмотрению новых проектов.</p></div>
{form_html("form")}</div></section>'''
    cp = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Контакты Event Network", "url": SITE + "/kontakty/", "about": {"@id": SITE + "/#org"}}
    write("/kontakty/", page("/kontakty/", f"Контакты {BRAND} — открыты к деловому сотрудничеству", f"Свяжитесь с Event Network: {EMAIL}{', ' + PHONE if PHONE else ''}. {ADDRESS}. {HOURS}. Обсудим задачи и формат сотрудничества.", body, "/kontakty/", [cp, ld_crumbs(it, "/kontakty/")]))

def build_privacy():
    it = [("/", "Главная"), (None, "Политика конфиденциальности")]
    S = [("1. Общие положения", f"Настоящая политика описывает, как {BRAND} (далее — Компания) обрабатывает персональные данные пользователей сайта {DOMAIN}. Используя сайт и отправляя формы, пользователь соглашается с условиями политики. Обработка данных осуществляется в соответствии с Законом Республики Казахстан «О персональных данных и их защите»."),
         ("2. Какие данные мы получаем", "Имя, номер телефона или адрес электронной почты, текст сообщения и выбранное направление — если пользователь указывает их в формах или в онлайн-чате. Также технические данные: сведения о браузере, устройстве и посещённых страницах, которые собирают сервисы веб-аналитики."),
         ("3. Цели обработки", "Ответ на обращение, обсуждение условий сотрудничества, подготовка коммерческого предложения, улучшение работы сайта."),
         ("4. Онлайн-ассистент", "Вопросы, которые пользователь задаёт в чате, передаются сервису искусственного интеллекта для формирования ответа. Не указывайте в чате сведения, которые не готовы передать. Контакты, оставленные в чате, используются только для связи по обращению."),
         ("5. Передача третьим лицам", "Компания не продаёт и не передаёт персональные данные третьим лицам, кроме случаев, предусмотренных законодательством Республики Казахстан, и сервисов, необходимых для работы сайта (хостинг, аналитика, доставка сообщений)."),
         ("6. Хранение и защита", "Данные хранятся не дольше, чем это необходимо для целей обработки. Компания принимает организационные и технические меры для защиты данных от несанкционированного доступа."),
         ("7. Права пользователя", f"Пользователь вправе запросить сведения о своих данных, их изменение или удаление, написав на {EMAIL}."),
         ("8. Файлы cookie", "Сайт использует cookie и аналогичные технологии для корректной работы и сбора обезличенной статистики. Их можно отключить в настройках браузера."),
         ("9. Изменения политики", f"Компания может обновлять политику. Актуальная редакция всегда опубликована на этой странице. Редакция от {datetime.date.today().strftime('%d.%m.%Y')}.")]
    body = f'''<section class="pb pb-s"><div class="wrap pb-in">{crumbs(it)}<h1>Политика конфиденциальности</h1><p>Как {BRAND} обрабатывает и защищает персональные данные пользователей сайта.</p></div></section>
<section class="sec"><div class="wrap prose">{"".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in S)}</div></section>'''
    write("/politika-konfidencialnosti/", page("/politika-konfidencialnosti/", f"Политика конфиденциальности — {BRAND}", f"Политика обработки персональных данных пользователей сайта {DOMAIN}.", body))

def build_404():
    body = f'''<section class="pb pb-s"><div class="wrap pb-in"><h1>Страница не найдена</h1><p>Возможно, она была перемещена или удалена. Перейдите на главную или выберите направление.</p><div class="btns"><a class="btn btn-g" href="/">На главную</a><a class="btn btn-ol" href="/napravleniya/">Все направления</a></div></div></section>
<section class="sec"><div class="wrap">{dir_cards()}</div></section>'''
    h = page("/404/", f"Страница не найдена — {BRAND}", "Страница не найдена.", body).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    write("/404/", h)

URLS = ["/", "/o-kompanii/", "/napravleniya/"] + [f'/napravleniya/{d["slug"]}/' for d in DIRS] + ["/portfolio/", "/kontakty/", "/politika-konfidencialnosti/"]

def build_meta():
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u == '/' else '0.8' if 'napravleniya' in u else '0.6'}</priority></url>\n" for u in URLS)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Bingbot", "YandexBot"]
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /api/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    ll = [f"# {BRAND}", "", f"> {INTRO[0]}", "", "## О компании"] + [f"- {t}" for t in ABOUT] + ["", "## Направления деятельности"]
    ll += [f"- [{d['name']}]({SITE}/napravleniya/{d['slug']}/): {d['text']}" for d in DIRS]
    ll += ["", "## Подход"] + [f"- {t}: {d}" for _, t, d in PRINCIPLES] + ["", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ_HOME]
    ll += ["", "## Контакты", f"- Электронная почта: {EMAIL}"] + ([f"- Телефон: {PHONE}"] if PHONE else []) + [f"- Адрес: {ADDRESS}", f"- Время работы: {HOURS}", f"- Сайт: {SITE}/"]
    (DIST / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": BRAND, "short_name": BRAND, "start_url": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#0b1b33", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")

def build_assets():
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8")
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    for f in ("favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        if (ROOT / "assets" / f).exists(): shutil.copy(ROOT / "assets" / f, DIST / f)

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_assets(); build_home(); build_about(); build_dirs(); build_portfolio(); build_contacts(); build_privacy(); build_404(); build_meta()
    print("pages:", len(URLS) + 1)
