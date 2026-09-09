# -*- coding: utf-8 -*-
"""index.html / privacy.html を「単一ファイルのプレビュー」に焼き直す。

やること
  - assets/css/site.css を <style> として本文に埋め込む
  - assets/js/games.js を <script> として本文に埋め込む
  - <img src="assets/img/..."> を縮小版の data URI に置き換える
      アイコン    128px 四方
      フィーチャー 幅 640
      スクショ     幅 360
      いずれも JPEG 品質 80
  - ページ間のリンク（index.html / privacy.html）は相対のまま残す（プレビューでは動かない）

出力
  dist/preview-index.html
  dist/preview-privacy.html

使い方
  python tools/build_preview.py
"""
import base64
import io
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

JPEG_QUALITY = 80
ICON_PX = 128
FEATURE_W = 640
SHOT_W = 360


def target_size(rel_path, orig):
    """画像の置き場所から、プレビュー用の寸法を決める。"""
    w, h = orig
    if "/icons/" in rel_path:
        return (ICON_PX, ICON_PX)
    if "/feature/" in rel_path:
        return (FEATURE_W, max(1, round(h * FEATURE_W / w)))
    if "/shots/" in rel_path:
        return (SHOT_W, max(1, round(h * SHOT_W / w)))
    return orig


def to_data_uri(rel_path, cache):
    if rel_path in cache:
        return cache[rel_path]
    abs_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    im = Image.open(abs_path)
    size = target_size(rel_path, im.size)
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    cache[rel_path] = uri
    return uri


def read(rel):
    with open(os.path.join(ROOT, rel.replace("/", os.sep)), "r", encoding="utf-8") as f:
        return f.read()


def build(src_name, out_name, cache):
    html = read(src_name)

    # CSS をインライン化
    css = read("assets/css/site.css")
    html = re.sub(
        r'<link rel="stylesheet" href="assets/css/site\.css">',
        "<style>\n" + css + "\n</style>",
        html,
    )

    # JS をインライン化
    if 'src="assets/js/games.js"' in html:
        js = read("assets/js/games.js")
        html = re.sub(
            r'<script src="assets/js/games\.js"></script>',
            "<script>\n" + js + "\n</script>",
            html,
        )

    # 画像を data URI へ
    def repl(m):
        return m.group(1) + to_data_uri(m.group(2), cache) + m.group(3)

    html = re.sub(r'(src=")(assets/img/[^"]+)(")', repl, html)

    # og:image も data URI にはせず、参照を落とす（プレビューでは意味がないため）
    html = re.sub(r'\s*<meta property="og:image"[^>]*>\n?', "\n", html)

    out_path = os.path.join(DIST, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def main():
    os.makedirs(DIST, exist_ok=True)
    cache = {}
    total = 0
    for src, out in (("index.html", "preview-index.html"),
                     ("privacy.html", "preview-privacy.html")):
        p = build(src, out, cache)
        size = os.path.getsize(p)
        total += size
        print("%-24s %8.1f KB" % (os.path.basename(p), size / 1024))
    print("%-24s %8.1f KB (上限 4096.0 KB)" % ("合計", total / 1024))
    if total > 4 * 1024 * 1024:
        raise SystemExit("プレビューの合計が 4MB を超えています")


if __name__ == "__main__":
    main()
