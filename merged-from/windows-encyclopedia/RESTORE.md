# RESTORE.md — самовоскрешение репозитория

## Что это за репо
Энциклопедия Windows 1985–2026 (6 эпох, версии, боли, продвижение, полюса ×20).
Приватный репо: github.com/rtynbirf/windows-encyclopedia.

## Восстановление из bundle
```bash
git clone windows-encyclopedia.bundle windows-encyclopedia
cd windows-encyclopedia
git remote add origin https://github.com/rtynbirf/windows-encyclopedia.git
git push -u origin main && git push --tags
```

## Где взять свежий bundle
1. Артефакт Actions: workflow `bundle-backup` (пн 03:00 UTC, 90 дней)
2. Локальные бандлы владельца: `windows-encyclopedia-fresh-*.bundle`

## Если репо на GitHub потеряно
Пересоздать приватным: github-runbook → 01-sozdanie-repo.md.

## Ключевые точки
- Тегов пока нет; первый тег — при следующем крупном пополнении
- Проверка после восстановления: CI-каркас (см. .github/workflows/ci.yml)
