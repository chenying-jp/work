#!/usr/bin/env python3
"""Download verified Union Hospital public images for p76."""
import os
import urllib.request

OUT = r"D:\11.Cursor\personal-ai-os\workspace\apps\career\portfolio\p76"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

# Verified public sources:
# - 39就医助手 协和环境照片
# - 163 协和内科综合楼报道配图 (2026-05)
# - 中新网 协和金银湖院区二期施工现场 (2023-12)
# - whuh.com 西院区门诊医技综合楼
IMAGES = [
    (
        "01.jpg",
        "https://pimg.39.net/PictureLib/A/f80/c9/20250114/org/1879095543926489109.jpg",
        "協和医院外観",
        "https://yyk.39.net/",
    ),
    (
        "02.jpg",
        "https://pimg.39.net/PictureLib/A/f80/c9/20250114/org/1879095557247598613.jpg",
        "協和医院院区",
        "https://yyk.39.net/",
    ),
    (
        "03.jpg",
        "http://dingyue.ws.126.net/2026/0511/3ec4e1ddj00teuex6003zd200u000mig00u000mi.jpg",
        "内科総合楼建設現場",
        "https://www.163.com/",
    ),
    (
        "04.jpg",
        "https://www.hb.chinanews.com/2023/1207/U1136P1DT20231207100508.jpg",
        "協和医院（金银湖院区）二期",
        "https://www.hb.chinanews.com/",
    ),
]

CAPTIONS_FILE = os.path.join(OUT, "captions.txt")


def download(name: str, url: str, referer: str) -> int:
    path = os.path.join(OUT, name)
    req = urllib.request.Request(url, headers={**HEADERS, "Referer": referer})
    with urllib.request.urlopen(req, timeout=40) as resp:
        data = resp.read()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def main():
    os.makedirs(OUT, exist_ok=True)
    caps = []
    for name, url, caption, referer in IMAGES:
        size = download(name, url, referer)
        caps.append(f"{name}\t{caption}")
        print(f"OK {name} {size} bytes - {caption}")

    with open(CAPTIONS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(caps))


if __name__ == "__main__":
    main()
