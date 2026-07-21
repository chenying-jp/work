# -*- coding: utf-8 -*-
import os, urllib.request
from PIL import Image

dst = r"D:\11.Cursor\personal-ai-os\workspace\apps\career\portfolio\p82"
# Hand-picked building photos from Archina article (skip maps/drawings)
urls = [
    # exterior after renovation (known good from earlier 02 before overwrite - use later exterior shots)
    "http://www.archina.com/uploadWX/20231215/657ba8a643c43170260291875514.jpeg",
    "http://www.archina.com/uploadWX/20231215/657ba8a65b9b5170260291832131.jpeg",
    "http://www.archina.com/uploadWX/20231215/657ba8a663f37170260291811175.jpeg",
    "http://www.archina.com/uploadWX/20231215/657ba8a5bafbd170260291756609.jpeg",
    "http://www.archina.com/uploadWX/20231215/657ba8a5bffd8170260291724512.jpeg",
]
referer = "http://www.archina.com/index.php?a=show&g=works&id=16906&m=index"
n = 2
for u in urls:
    if n > 4:
        break
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Referer": referer})
        path = os.path.join(dst, "_t.bin")
        with urllib.request.urlopen(req, timeout=40) as r:
            open(path, "wb").write(r.read())
        im = Image.open(path).convert("RGB")
        w, h = im.size
        aspect = w / float(h)
        print("got", w, h, round(aspect, 2), u[-45:])
        if aspect > 2.0:  # skip maps
            os.remove(path)
            continue
        if max(w, h) > 1600:
            if w >= h:
                im = im.resize((1600, int(h * 1600 / w)), Image.LANCZOS)
            else:
                im = im.resize((int(w * 1600 / h), 1600), Image.LANCZOS)
        out = os.path.join(dst, f"{n:02d}.jpg")
        im.save(out, "JPEG", quality=85, optimize=True)
        os.remove(path)
        print("saved", out)
        n += 1
    except Exception as e:
        print("fail", e)
