"""Audit image path case mismatches (GitHub Pages is case-sensitive)."""
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = Path(r"D:\11.Cursor\debug-86cf1a.log")
BASE = "https://chenying-jp.github.io/work/"


def log(hypothesis_id: str, message: str, data: dict) -> None:
    entry = {
        "sessionId": "86cf1a",
        "runId": "pre-fix",
        "hypothesisId": hypothesis_id,
        "location": "audit_image_case.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def head(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


refs = []
for html in ROOT.glob("*.html"):
    text = html.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:src|data-src)="([^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))"', text):
        refs.append((html.name, m.group(1)))

mismatches = []
for html_name, ref in refs:
    path = ROOT / ref.replace("/", "\\")
    if not path.exists():
        alt = ROOT / ref
        if alt.exists():
            mismatches.append({"html": html_name, "ref": ref, "actual": ref, "issue": "path_ok"})
        else:
            parent = path.parent
            if parent.is_dir():
                name = path.name
                for f in parent.iterdir():
                    if f.name.lower() == name.lower() and f.name != name:
                        mismatches.append({"html": html_name, "ref": ref, "actual": str(f.relative_to(ROOT)).replace("\\", "/"), "issue": "case_mismatch"})
                        break

log("H1", "case_mismatch_scan", {"mismatches": mismatches})

for item in mismatches:
    ref_url = BASE + item["ref"]
    actual_url = BASE + item["actual"]
    log("H1", "http_check", {
        "ref": item["ref"],
        "ref_status": head(ref_url),
        "actual": item["actual"],
        "actual_status": head(actual_url),
    })

print(json.dumps({"mismatches": mismatches}, ensure_ascii=False, indent=2))
