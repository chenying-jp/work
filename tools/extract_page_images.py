#!/usr/bin/env python3
import re
import urllib.request

URLS = [
    "https://design.citic/portal/article/index/id/3816.html",
    "https://www.whuh.com/info/1021/12352.htm",
    "http://news.cnhubei.com/content/2023-06/21/content_16038338.html",
    "http://www.hb.chinanews.com.cn/news/2023/1207/400023.html",
    "https://www.whuh.com/info/21314/72566.htm",
]

for url in URLS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
        imgs = re.findall(r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp)[^"\']*)["\']', html, re.I)
        imgs += re.findall(r'data-src=["\']([^"\']+)["\']', html, re.I)
        imgs += re.findall(r'original=["\']([^"\']+)["\']', html, re.I)
        print("===", url)
        seen = set()
        for im in imgs:
            if im in seen:
                continue
            seen.add(im)
            if im.startswith("//"):
                im = "https:" + im
            print(" ", im[:180])
    except Exception as e:
        print("ERR", url, e)
