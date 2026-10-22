"""Баннеры превью для каждой страницы: assets/img/og/<файл>.jpg (нужен Playwright).
Перерисовываются только изменившиеся (кэш в manifest.json)."""
import base64, hashlib, json, pathlib, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import OG, LOGO_MARK, E
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"; OUT = A / "img" / "og"; OUT.mkdir(parents=True, exist_ok=True)
OGV = "2"
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
fonts = "".join(f'@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(A / "fonts" / f)})}}'
                for fam, w, f in [("H", 800, "manrope-cyrillic-800-normal.woff2"), ("HL", 800, "manrope-latin-800-normal.woff2"),
                                  ("T", 500, "onest-cyrillic-500-normal.woff2"), ("TL", 500, "onest-latin-500-normal.woff2")])
mark = LOGO_MARK.replace('class="logo-m"', 'width="100%" height="100%"')

def html(title, sub, bg):
    size = 76 if len(title) <= 28 else 64 if len(title) <= 44 else 56
    return f'''<html><head><style>{fonts}
body{{margin:0}}.b{{width:1200px;height:630px;position:relative;overflow:hidden;background:#0b1b33;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff}}
.bg{{position:absolute;inset:0;background:url(data:image/webp;base64,{b64(A / "img" / (bg + ".webp"))}) center/cover;opacity:1}}
.sh{{position:absolute;inset:0;background:radial-gradient(ellipse 52% 48% at 50% 52%,rgba(6,15,32,.78),rgba(6,15,32,.35) 80%,rgba(6,15,32,.15))}}
.c{{position:relative;width:1000px;display:flex;flex-direction:column;align-items:center}}
.l{{display:flex;align-items:center;gap:14px;font-family:HL,H;font-weight:800;font-size:22px;letter-spacing:.1em;line-height:1.05;text-align:left;margin-bottom:38px}}
.l .m{{width:58px;height:58px}}
h1{{margin:0;font-family:H,HL;font-weight:800;font-size:{size}px;line-height:1.12;letter-spacing:-.01em;text-wrap:balance}}
.ln{{width:72px;height:3px;background:#c9a35c;border-radius:2px;margin:30px 0 24px}}
p{{margin:0;font-family:T,TL;font-weight:500;font-size:27px;color:#e8cf9b}}
</style></head><body><div class="b"><div class="bg"></div><div class="sh"></div><div class="c">
<div class="l"><div class="m">{mark}</div><div>EVENT<br>NETWORK</div></div><h1>{E(title)}</h1><div class="ln"></div><p>{E(sub)}</p></div></div></body></html>'''

man_p = OUT / "manifest.json"
man = json.loads(man_p.read_text()) if man_p.exists() else {}
n = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    for url, (slug, title, sub, bg) in OG.items():
        key = hashlib.md5((OGV + title + sub + bg).encode()).hexdigest()
        out = OUT / f"{slug}.jpg"
        if man.get(slug) == key and out.exists(): continue
        pg.set_content(html(title, sub, bg)); pg.wait_for_timeout(150)
        pg.screenshot(path=str(out), type="jpeg", quality=86); man[slug] = key; n += 1
    b.close()
man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1))
print("og:", len(OG), "rendered:", n)
