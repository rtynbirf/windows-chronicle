# KNOWN_ISSUES · windows-chronicle · Волна ×5 (2026-11-09)

## Красные CI (было → после патча)

| Run | Что было | Диагноз | После |
|---|---|---|---|
| 42312232454 (11-06 23:29) | guardian-tripwire failure, **0 jobs**, имя рана = путь к файлу | общий корень кластера ×5: пин-склейка `# vXwith:` в tripwire.yml SHA d9d4d4a3 (PyYAML-репро, строки 39–41) | волна ×4 переписала: зелёный **42517297661** @ f95b9b40 (19:53); ×5-D диспатч: run ****42527378709** (workflow_dispatch → success, 21:52, sha f95b9b40)** |
| 42312388044 (11-06 23:30) | Dependabot dynamic «github_actions in / for actions/github-script - Update» failure | НЕ «битый uses-пин/кириллица»: `dependency_file_not_parseable` — tripwire.yml того SHA не парсился (та же склейка `# vXwith:`), Dependabot не смог обновить PR #2 | yml починен волной ×4; PR #2 влит (github-script v9.0.0 в HEAD); Dependabot повторит по weekly-расписанию ⬜ |
| 42312387848 (11-06 23:30) | Dependabot dynamic «github_actions in / for actions/checkout - Update» failure | то же: `dependency_file_not_parseable` на tripwire.yml, PR #1 (checkout) | PR #1 влит (checkout v7.0.1 в HEAD); weekly-тик Dependabot должен пройти ⬜ |

## Квирки
- Сигнатуру «invalid workflow file» видно по трём признакам сразу: имя рана = ПУТЬ к файлу, jobs total_count = 0, GET /runs/{id}/logs → 404. Логи Dependabot при этом живы — в них и сидел настоящий диагноз.
- Кириллица в yml НЕ была причиной (в файле SHA d9d4d4a3 кириллица легитимна в name/echo и парсится).
