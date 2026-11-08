# -*- coding: utf-8 -*-
"""scripts/csv_to_jsonld.py — конвертер data/timeline.csv → data/chronicle.jsonld.

П57 (issue #6): события хроники становятся машинно-читаемым JSON-LD
(schema.org/Event в @graph). Источник истины — data/timeline.csv
(41 запись, разделитель «;», кодировка UTF-8 c BOM).

Детерминировано: один вход → байт-в-байт один выход (ключи и порядок
полей зафиксированы, indent=2, ensure_ascii=False, финальный \\n).

Запуск:  python3 scripts/csv_to_jsonld.py [--check]
  без флага — перезаписать data/chronicle.jsonld;
  --check   — rc=0, если файл уже соответствует CSV (нет дрейфа данных).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "timeline.csv"
JSONLD_PATH = ROOT / "data" / "chronicle.jsonld"


def load_events() -> list[dict]:
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh, delimiter=";"))
    if not rows:
        raise SystemExit("timeline.csv пуст")
    header = rows[0]
    data = [r for r in rows[1:] if any(cell.strip() for cell in r)]
    if header != ["дата", "версия/событие", "линия", "примечание", "теги"]:
        raise SystemExit(f"неожиданная шапка CSV: {header}")
    events = []
    for i, (date, name, line, note, tags) in enumerate(data, 1):
        date, name, line = date.strip(), name.strip(), line.strip()
        note, tags = note.strip(), tags.strip()
        node = {
            "@type": "Event",
            "@id": f"#event-{i:03d}",
            "identifier": f"WC-E{i:03d}",
            "name": name,
            "startDate": date,
            "about": line,
        }
        if note:
            node["description"] = note
        if tags:
            node["keywords"] = ", ".join(t.strip() for t in tags.split(",") if t.strip())
        events.append(node)
    return events


def build_doc(events: list[dict]) -> dict:
    dates = sorted(e["startDate"] for e in events)
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Windows Chronicle · хроника событий 1985–2026",
        "description": (
            "Машинный таймлайн хроники Windows: релизы, вехи жизненного цикла, "
            "метрики доли и побочные линии. Составлен из data/timeline.csv "
            f"({len(events)} событий) скриптом scripts/csv_to_jsonld.py."
        ),
        "creator": {"@type": "Organization", "name": "windows-chronicle (rtynbirf)"},
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "temporalCoverage": f"{dates[0]}/{dates[-1]}",
        "isBasedOn": "data/timeline.csv",
        "@graph": events,
    }


def serialize(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str]) -> int:
    events = load_events()
    text = serialize(build_doc(events))
    if "--check" in argv:
        if not JSONLD_PATH.exists():
            print(f"FAIL  {JSONLD_PATH.name} отсутствует")
            return 1
        if JSONLD_PATH.read_text(encoding="utf-8") == text:
            print(f"PASS  chronicle.jsonld == timeline.csv ({len(events)} событий, дрейфа нет)")
            return 0
        print("FAIL  chronicle.jsonld разошёлся с data/timeline.csv — пересобери")
        return 1
    JSONLD_PATH.write_text(text, encoding="utf-8")
    print(f"OK    data/chronicle.jsonld: {len(events)} событий schema.org/Event "
          f"из data/timeline.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
