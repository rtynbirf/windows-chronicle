# TODO · windows-chronicle

> Живой трекер-мемо Волны ×5 (2026-11-09). Полный реестр аккаунта: github-runbook → РЕЕСТР-НЕДОДЕЛАННОГО-2026-11-09.md · мастер-индекс: github-runbook#10.

## 🌊 Волна ×5 · 2026-11-09 · субагент ×5-D «Хаб и стражи»

### 1) Открытые issues
- [#5](https://github.com/rtynbirf/windows-chronicle/issues/5) 🧾 КОСЯКИ · аудит 2026-11-08 — открыт; обновлён пломбой ×5-D.

### 2) Честные хвосты ⬜
- ⬜ **Dependabot-красные 42312388044/42312387848 (11-06 23:30)** — гипотеза задания «битый uses-пин или кириллица в yml» уточнена: настоящий диагноз `dependency_file_not_parseable: /.github/workflows/guardian-tripwire.yml not parseable` — Dependabot не смог распарсить тогда ещё склеенный `# vXwith:` yml при обновлении PR #1 (actions/checkout) и #2 (actions/github-script). Принудительно перезапустить Dependabot из API нельзя; PR #1/#2 влиты, tripwire.yml на HEAD парсится, оба пина (v7.0.1 checkout, v9.0.0 github-script) подтверждены живым прогоном 42517297661. Ожидаем зелёный на ближайшем weekly-цикле Dependabot — проверить следующей волне.
- ⬜ П-57 (JSON-LD таймлайн) добит f95b9b4; браузерные пробы рендера — следующая волна.

### 3) Что делать следующей волне
- Проверить статус Dependabot после weekly-тика: /actions/runs?event=dynamic — оба «Update» должны стать success.
- КОСЯКИ #5 закрывать по закону: только после живых зелёных прогонов всего перечисленного.
