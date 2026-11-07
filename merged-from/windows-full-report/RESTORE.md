# RESTORE.md — самовоскрешение репозитория

## Что это за репо
Полный верифицированный отчёт по истории Windows 1985–2026 (главный список
40 пунктов между полюсами). Приватный репо: github.com/rtynbirf/windows-full-report.

## Восстановление из bundle (полный клон: ветки + теги)
```bash
git clone windows-full-report.bundle windows-full-report
cd windows-full-report
git remote add origin https://github.com/rtynbirf/windows-full-report.git
git push -u origin main && git push --tags
```

## Где взять свежий bundle
1. Артефакт Actions: workflow `bundle-backup` (пн 03:00 UTC, 90 дней)
2. Локальные бандлы владельца: `windows-full-report-fresh-*.bundle`

## Если репо на GitHub потеряно
Пересоздать приватным: github-runbook → 01-sozdanie-repo.md.

## Ключевые точки
- Тегов пока нет; первый тег `v0.1.0` — при следующем крупном пополнении
- Проверка после восстановления: CI-инварианты (см. .github/workflows/ci.yml)
