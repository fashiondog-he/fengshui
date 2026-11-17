"""Scan user-facing copy for disallowed fortune-telling marketing language.

Classifier internals are intentionally outside the scan scope: they need to
recognize unsafe requests so the boundary can refuse them.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = (ROOT / "README.md", ROOT / "prompts", ROOT / "ui", ROOT / "copy")
DISALLOWED = ("算命", "预测", "转运", "开运", "化解", "灵验", "精准断命")


def scan() -> list[str]:
    findings: list[str] = []
    files = [p for root in SCAN_ROOTS if root.exists()
             for p in ([root] if root.is_file() else root.rglob("*"))
             if p.is_file() and p.suffix.lower() in {".md", ".txt", ".html", ".json"}]
    for path in files:
        content = path.read_text(encoding="utf-8")
        for term in DISALLOWED:
            if term in content:
                findings.append(f"{path.relative_to(ROOT)}: 命中用户文案禁用词")
    return findings


if __name__ == "__main__":
    results = scan()
    if results:
        print("\n".join(results))
        sys.exit(1)
    print("用户面向文案禁用词扫描通过")
