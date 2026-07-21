import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = """
<nav class="site-nav">
  <div class="site-nav-inner">
    <a class="brand" href="index.html">陳 穎</a>
    <a href="index.html">ホーム</a>
    <a href="career.html">職務経歴</a>
    <a href="index.html#projects" class="active">施工実績</a>
    <a href="credentials.html">資格</a>
    <a href="activities.html">活動</a>
  </div>
</nav>
"""

TITLES = {
    "p88.html": "硚口区 漢江湾全民フィットネスセンター",
    "p27.html": "中天建設・金科城 K2地块 一期",
    "p81.html": "開発区第一初級中学（神龍校区）",
    "p76.html": "協和医院 陽子線センター",
    "p66.html": "中天建設・金科城 K2地块 二期",
    "p32.html": "武漢建工・洪山三小",
    "p90.html": "路德環保 アスファルト舗装",
    "p16.html": "武漢建工・流芳新鎮G地块",
}

for fn, title in TITLES.items():
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    if "site-nav" in html:
        print("skip", fn)
        continue
    if "assets/site.css" not in html:
        html = html.replace(
            '<meta name="viewport"',
            '<link rel="stylesheet" href="assets/site.css">\n<meta name="viewport"',
            1,
        )
    html = html.replace("<body>", "<body>\n" + NAV, 1)
    crumb = (
        f'<p class="breadcrumb"><a href="index.html">ホーム</a> › '
        f'<a href="index.html#projects">施工実績</a> › {title}</p>\n\n'
    )
    html = html.replace("<main>", "<main>\n\n" + crumb, 1)
    html = html.replace(
        "施工管理ポートフォリオ — ローカル版",
        "就活プロフィール — ローカル版 · 2026",
    )
    html = html.replace("← 実績一覧に戻る", "← 施工実績一覧に戻る")
    open(path, "w", encoding="utf-8").write(html)
    print("patched", fn)
