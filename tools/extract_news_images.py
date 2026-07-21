#!/usr/bin/env python3
import re
import urllib.request

URLS = [
    "http://c.m.163.com/news/a/KSKL317P0534FOQ8.html",
    "https://www.163.com/dy/article/KSJPMF8S0514BINQ.html",
    "https://yyk.39.net/wuhan/532c9/picture.html",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}


def extract(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    print("===", url, "len", len(html))
    patterns = [
        r'data-src=["\']([^"\']+)["\']',
        r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp)[^"\']*)["\']',
        r'"(https?://[^"\s]+\.(?:jpg|jpeg|png))"',
        r'url\((https?://[^)]+)\)',
    ]
    seen = set()
    for pat in patterns:
        for m in re.findall(pat, html, re.I):
            if m.startswith("//"):
                m = "https:" + m
            if any(x in m for x in ["logo", "icon", "avatar", "emoji", "share", "btn", "qrcode"]):
                continue
            if m not in seen:
                seen.add(m)
                print(" ", m[:200])


for u in URLS:
    try:
        extract(u)
    except Exception as e:
        print("ERR", u, e)
