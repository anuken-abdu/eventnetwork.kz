"""Favicon, иконки и OG-баннер из логотипа (нужен Playwright)."""
import pathlib, base64, sys
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import LOGO_MARK
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"
f = lambda n: base64.b64encode((A / "fonts" / n).read_bytes()).decode()
mark = LOGO_MARK.replace('class="logo-m"', 'width="100%" height="100%"')
icon_html = f'<html><body style="margin:0"><div style="width:512px;height:512px;background:#0b1b33;border-radius:0;display:flex;align-items:center;justify-content:center"><div style="width:330px;height:330px">{mark}</div></div></body></html>'
og_bg = base64.b64encode((A / "img" / "og-base.png").read_bytes()).decode()
og_html = f'''<html><head><style>
@font-face{{font-family:M;font-weight:800;src:url(data:font/woff2;base64,{f("manrope-cyrillic-800-normal.woff2")})}}
@font-face{{font-family:ML;font-weight:800;src:url(data:font/woff2;base64,{f("manrope-latin-800-normal.woff2")})}}
@font-face{{font-family:O;font-weight:500;src:url(data:font/woff2;base64,{f("onest-cyrillic-500-normal.woff2")})}}
body{{margin:0}}.b{{width:1200px;height:630px;background:url(data:image/png;base64,{og_bg});position:relative;font-family:ML,M,sans-serif;color:#fff}}
.l{{position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:16px;font-weight:800;font-size:24px;letter-spacing:.08em;line-height:1.05}}
.l .m{{width:64px;height:64px}}
h1{{position:absolute;left:80px;top:200px;width:700px;margin:0;font-family:M,ML;font-weight:800;font-size:58px;line-height:1.12}}
p{{position:absolute;left:80px;bottom:76px;margin:0;font-family:O;font-size:24px;color:#e8cf9b}}
</style></head><body><div class="b"><div class="l"><div class="m">{mark}</div><div>EVENT<br>NETWORK</div></div>
<h1>Объединяем технологии, информацию и возможности</h1><p>eventnetwork.kz</p></div></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 512, "height": 512})
    pg.set_content(icon_html); pg.screenshot(path=str(A / "icon-512.png"))
    im = Image.open(A / "icon-512.png").convert("RGB")
    im.resize((192, 192), Image.LANCZOS).save(A / "icon-192.png")
    im.resize((180, 180), Image.LANCZOS).save(A / "apple-touch-icon.png")
    im.resize((48, 48), Image.LANCZOS).save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    pg2 = b.new_page(viewport={"width": 1200, "height": 630}); pg2.set_content(og_html); pg2.wait_for_timeout(300)
    pg2.screenshot(path=str(A / "img" / "og.jpg"), type="jpeg", quality=86)
    b.close()
(A / "img" / "og-base.png").unlink(missing_ok=True)
print("ok")
