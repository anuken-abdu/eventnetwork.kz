# Event Network — сайт eventnetwork.kz

Статический сайт (папка `dist/`) + две функции Vercel (`api/`).

## Структура
- `dist/` — готовый сайт, его отдаёт Vercel (14 страниц, sitemap, robots, llms.txt).
- `api/chat.js` — ИИ-ассистент (Anthropic). `api/lead.js` — заявки в Telegram.
- `src/data.py` — все тексты и контакты. `src/build.py` — генератор страниц.
- `src/app.js` — скрипты сайта. `assets/` — стили, шрифты, иллюстрации, иконки.
- `src/art.html`, `src/render_art.py`, `src/render_brand.py` — генерация иллюстраций, favicon и OG-баннера.

## Переменные окружения (Vercel → Settings → Environment Variables)
| Переменная | Зачем |
|---|---|
| `ANTHROPIC_API_KEY` | умные ответы ИИ-ассистента. Без ключа чат работает на встроенной базе ответов |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | заявки из формы и чата приходят в Telegram. Без них форма открывает письмо на почту |
| `CONTACT_EMAIL`, `CONTACT_PHONE` | контакты, которые называет ассистент (по умолчанию info@eventnetwork.kz) |

## Как поменять контакты или тексты
1. Отредактировать `src/data.py` (PHONE, WHATSAPP, EMAIL, ADDRESS, HOURS, GA_ID).
2. `python3 src/build.py` — пересобрать `dist/`.
3. Залить изменённые файлы в репозиторий.

Перерисовать иллюстрации: `python3 src/render_art.py && python3 src/render_brand.py` (нужен Playwright).

## Домен (hoster.kz → Vercel)
DNS-записи домена eventnetwork.kz:
- `A` `@` → `76.76.21.21`
- `CNAME` `www` → `cname.vercel-dns.com`
