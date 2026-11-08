# -*- coding: utf-8 -*-
"""scripts/build_timeline.py — генератор HTML-таймлайна из data/chronicle.jsonld.

П57 (issue #6): JSON-LD (schema.org/Event) → детерминированный HTML.
Двойная сборка обязана быть байт-в-байт идентичной: в выводе нет времени
сборки, случайных id и внешних ресурсов (страница работает офлайн).

Приёмка (машинная, --selftest):
  1) JSON-LD валиден: парсится json'ом, @context/@type/@graph на месте,
     каждое событие — Event с name и startDate;
  2) двойная сборка идентична;
  3) число событий в HTML == числу событий в JSON-LD.

Запуск:
  python3 scripts/build_timeline.py            # собрать timeline.html
  python3 scripts/build_timeline.py --selftest # самопроверка (rc=0/1)
"""
from __future__ import annotations

import html
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONLD_PATH = ROOT / "data" / "chronicle.jsonld"
HTML_PATH = ROOT / "timeline.html"

LINE_CLASSES = {
    "клиент": "line-client",
    "сервер": "line-server",
    "побочная": "line-side",
    "служебное": "line-service",
    "метрика": "line-metric",
    "жизненный цикл": "line-lifecycle",
}


def load_and_validate(path: Path) -> list[dict]:
    """Парсер + структурная валидация JSON-LD. rc!=0 при любом отступлении."""
    doc = json.loads(path.read_text(encoding="utf-8"))          # parser rc=0
    if doc.get("@context") != "https://schema.org":
        raise ValueError("@context должен быть https://schema.org")
    if doc.get("@type") != "Dataset":
        raise ValueError("@type корня должен быть Dataset")
    graph = doc.get("@graph")
    if not isinstance(graph, list) or not graph:
        raise ValueError("@graph — непустой массив")
    for i, node in enumerate(graph):
        if node.get("@type") != "Event":
            raise ValueError(f"@graph[{i}]: не Event")
        for field in ("name", "startDate"):
            if not node.get(field):
                raise ValueError(f"@graph[{i}]: нет {field}")
    return graph


def render(graph: list[dict]) -> str:
    items = []
    for node in graph:
        cls = LINE_CLASSES.get(str(node.get("about", "")).lower(), "line-other")
        date = html.escape(str(node["startDate"]))
        name = html.escape(str(node["name"]))
        line = html.escape(str(node.get("about", "")))
        parts = [f'<time>{date}</time>', f'<span class="line {cls}">{line}</span>']
        if node.get("description"):
            parts.append(f'<p class="note">{html.escape(str(node["description"]))}</p>')
        if node.get("keywords"):
            tags = "".join(
                f'<code>{html.escape(t.strip())}</code>'
                for t in str(node["keywords"]).split(",")
            )
            parts.append(f'<p class="tags">{tags}</p>')
        items.append(
            f'    <li class="event" id="{html.escape(str(node["identifier"]))}">\n'
            f'      <strong class="title">{name}</strong>\n'
            f'      <div class="meta">{"".join(parts[:2])}</div>\n'
            + "".join(f"      {p}\n" for p in parts[2:])
            + "    </li>"
        )
    body = "\n".join(items)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Хроника Windows · 1985–2026 · таймлайн</title>
<style>
:root {{ --ink:#1b2733; --muted:#5a6b7b; --bg:#f7f9fb; --card:#ffffff; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; padding:2rem 1rem; font:16px/1.55 system-ui, sans-serif;
       color:var(--ink); background:var(--bg); }}
main {{ max-width:52rem; margin:0 auto; }}
h1 {{ font-size:1.5rem; margin:0 0 .25rem; }}
.sub {{ color:var(--muted); margin:0 0 1.5rem; }}
ol.timeline {{ list-style:none; margin:0; padding:0 0 0 1.25rem;
       border-left:2px solid #d4dde6; }}
li.event {{ position:relative; margin:0 0 1rem; padding:.75rem 1rem;
       background:var(--card); border:1px solid #e3e9ef; border-radius:10px; }}
li.event::before {{ content:""; position:absolute; left:-1.72rem; top:1.15rem;
       width:10px; height:10px; border-radius:50%; background:#2f6db3;
       border:2px solid var(--bg); }}
.title {{ font-size:1.05rem; }}
.meta time {{ font-variant-numeric:tabular-nums; color:var(--muted);
       margin-right:.6rem; }}
.line {{ font-size:.8rem; padding:.1rem .5rem; border-radius:999px;
       background:#eaf1f8; color:#2f6db3; }}
.line-server {{ background:#eaf5ec; color:#2e7d43; }}
.line-side {{ background:#f6eefa; color:#7a4bab; }}
.line-service {{ background:#f4f1e9; color:#8a6d1f; }}
.line-metric {{ background:#e9f4f6; color:#1f7a8c; }}
.line-lifecycle {{ background:#f9ebe9; color:#a8402f; }}
.note {{ margin:.45rem 0 0; color:var(--muted); }}
.tags {{ margin:.45rem 0 0; }}
.tags code {{ font-size:.75rem; background:#eef2f6; border-radius:4px;
       padding:.05rem .3rem; margin-right:.3rem; }}
footer {{ margin-top:1.5rem; color:var(--muted); font-size:.85rem; }}
</style>
</head>
<body>
<main>
  <h1>Хроника Windows · 1985–2026</h1>
  <p class="sub">Таймлайн, сгенерированный из машинных данных
     <code>data/chronicle.jsonld</code> (schema.org/Event) скриптом
     <code>scripts/build_timeline.py</code>. Детерминированная сборка:
     двойной прогон байт-в-байт идентичен.</p>
  <ol class="timeline">
{body}
  </ol>
  <footer>Источники и метод — <a href="06-sources/sources.md">06-sources</a>;
     данные — <a href="data/chronicle.jsonld">data/chronicle.jsonld</a>.</footer>
</main>
</body>
</html>
"""


def count_events_in_html(html_text: str) -> int:
    return html_text.count('<li class="event" id=')


def main(argv: list[str]) -> int:
    graph = load_and_validate(JSONLD_PATH)
    page = render(graph)
    if "--selftest" in argv:
        ok = True
        # 1) парсинг/валидация уже прошли (rc был бы != 0 иначе)
        print(f"PASS  JSON-LD валиден: {len(graph)} событий schema.org/Event, "
              f"@context/@type/@graph на месте")
        # 2) двойная сборка идентична
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.html", Path(tmp) / "b.html"
            a.write_text(page, encoding="utf-8")
            page2 = render(load_and_validate(JSONLD_PATH))
            b.write_text(page2, encoding="utf-8")
            same = a.read_bytes() == b.read_bytes()
        ok &= same
        print(f"{'PASS' if same else 'FAIL'}  двойная сборка "
              f"{'байт-в-байт идентична' if same else 'РАЗОШЛАСЬ'}")
        # 3) число событий в HTML == числу в JSON-LD
        n_html = count_events_in_html(page)
        count_ok = n_html == len(graph)
        ok &= count_ok
        print(f"{'PASS' if count_ok else 'FAIL'}  событий в HTML ({n_html}) == "
              f"в JSON-LD ({len(graph)})")
        print(f"# Result: {'SELFTEST GREEN' if ok else 'SELFTEST RED'}")
        return 0 if ok else 1
    HTML_PATH.write_text(page, encoding="utf-8")
    print(f"OK    timeline.html: {count_events_in_html(page)} событий из "
          f"{len(graph)} в JSON-LD")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
