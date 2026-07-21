#!/usr/bin/env python3
"""Fetch image URLs from Baidu image search."""
import json
import re
import sys
import urllib.parse
import urllib.request

WORD = "武汉建工 协和医院 综合住院楼二期 工程照片"


def fetch_acjson(word: str, pn: int = 0, rn: int = 30) -> list[dict]:
    params = {
        "tn": "resultjson_com",
        "logid": "1",
        "ipn": "rj",
        "ct": "201326592",
        "fp": "result",
        "queryWord": word,
        "word": word,
        "pn": str(pn),
        "rn": str(rn),
        "ie": "utf-8",
        "oe": "utf-8",
    }
    url = "https://image.baidu.com/search/acjson?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://image.baidu.com/",
            "Accept": "application/json, text/plain, */*",
        },
    )
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    start = raw.find("{")
    obj = json.loads(raw[start:])
    items = []
    for it in obj.get("data", []):
        if isinstance(it, dict) and (it.get("thumbURL") or it.get("middleURL") or it.get("objURL")):
            items.append(it)
    return items


def fetch_html(word: str) -> list[str]:
    url = "https://image.baidu.com/search/index?tn=baiduimage&word=" + urllib.parse.quote(word)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    urls = []
    for pat in [
        r'"objURL":"(https?://[^"]+)"',
        r'"middleURL":"(https?://[^"]+)"',
        r'"thumbURL":"(https?://[^"]+)"',
        r'"(https?://[^"\s]+\.(?:jpg|jpeg|png))"',
    ]:
        for m in re.findall(pat, html, re.I):
            u = m.replace("\\/", "/")
            if "baidu.com" not in u and "bdstatic.com" not in u:
                urls.append(u)
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def main():
    word = sys.argv[1] if len(sys.argv) > 1 else WORD
    print("query:", word)
    try:
        items = fetch_acjson(word)
        print("acjson items:", len(items))
        for i, it in enumerate(items[:20]):
            title = (it.get("fromPageTitleEnc") or it.get("fromPageTitle") or "")[:80]
            url = it.get("middleURL") or it.get("objURL") or it.get("thumbURL")
            print(f"{i}\t{title}\t{url}")
    except Exception as e:
        print("acjson error:", e)

    try:
        urls = fetch_html(word)
        print("html urls:", len(urls))
        for u in urls[:20]:
            print(u)
    except Exception as e:
        print("html error:", e)


if __name__ == "__main__":
    main()
