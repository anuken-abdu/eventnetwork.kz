"""Рендерит иллюстрации из src/art.html в assets/img/*.webp (нужен Playwright)."""
import base64, io, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
JOBS = [  # имя, ширина, высота, seed, качество
    ("hero", 2000, 1000, 7, 82), ("about", 1800, 760, 11, 80), ("quote", 1800, 560, 5, 80),
    ("contacts", 1800, 600, 3, 80), ("portfolio", 1800, 600, 9, 80), ("og", 1200, 630, 7, 85),
    ("digital", 960, 640, 21, 80), ("security", 960, 640, 22, 80), ("analytics", 960, 640, 23, 80),
    ("marketing", 960, 640, 24, 80), ("events", 960, 640, 25, 80), ("culture", 960, 640, 26, 80),
    ("support", 960, 640, 27, 80),
]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto((ROOT / "src" / "art.html").as_uri())
    for name, w, h, seed, q in JOBS:
        data = pg.evaluate(f"render('{name}', {w}, {h}, {seed})")
        im = Image.open(io.BytesIO(base64.b64decode(data.split(",", 1)[1]))).convert("RGB")
        if name == "og":
            im.save(OUT / "og-base.png")
        else:
            im.save(OUT / f"{name}.webp", quality=q, method=6)
        print(name, im.size)
    b.close()
