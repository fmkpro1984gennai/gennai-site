# -*- coding: utf-8 -*-
"""OUTBOX の原本から、サイト用の画像を生成する（原本は読むだけ）。"""
import os
from PIL import Image

SRC = r"C:\Users\fmkpr\OneDrive\Desktop\Work\OUTBOX"
DST = r"E:\service_gennai_site\assets\img"

SLUGS = ["ponpon-tile", "mizumichi-tsunagi", "nakamahazure-jump",
         "yajirushi-daidasshutsu", "quiz-tobiishi", "irowake-labo",
         "balance-koujou", "gattai-danball"]

report = []

for slug in SLUGS:
    if slug == "ponpon-tile":
        icon_src = os.path.join(SRC, "ponpon-tile-icon", "ponpon-tile_icon_1024_appstore.png")
    else:
        icon_src = os.path.join(SRC, slug + "-icon", "final", "icon_1024_appstore.png")
    im = Image.open(icon_src)
    report.append(("icon-src", slug, im.size, im.mode))
    im = im.convert("RGB")
    for px in (256, 128):
        out = os.path.join(DST, "icons", "%s-%d.png" % (slug, px))
        im.resize((px, px), Image.LANCZOS).save(out, "PNG", optimize=True)

    feat_src = os.path.join(SRC, slug + "-store", "googleplay", "feature_graphic_1024x500.png")
    fi = Image.open(feat_src)
    report.append(("feature-src", slug, fi.size, fi.mode))
    fi = fi.convert("RGB")
    out = os.path.join(DST, "feature", slug + ".jpg")
    fi.save(out, "JPEG", quality=85, optimize=True, progressive=True)

for i in range(1, 5):
    s = os.path.join(SRC, "ponpon-tile-store", "googleplay", "v2", "export-final", "gp", "gp_%d.png" % i)
    im = Image.open(s)
    report.append(("shot-src", "gp_%d" % i, im.size, im.mode))
    im = im.convert("RGB")
    w = 540
    h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(
        os.path.join(DST, "shots", "ponpon-tile", "gp_%d.jpg" % i),
        "JPEG", quality=85, optimize=True, progressive=True)
    print("shot gp_%d -> %dx%d" % (i, w, h))

for r in report:
    print(r)
