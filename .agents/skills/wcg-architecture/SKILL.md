---
name: wcg-architecture
description: >
  Start-here map of word-calendar-generator: what the app is, the data flow from CLI args to
  generated .docx, module ownership, the one-page fit budget, invariants and which domain
  skill to load for which change. Use when starting any work here, when unsure which skill
  applies, or when a change touches multiple domains.
---

# wcg-architecture

## What it is
A Typer CLI (Python 3.14, uv) that generates printable A4 Word calendars: one page per
month, a bordered 7-column Mon-Sun grid with one tall row per week. Users run
`word-calendar-generator generate MONTH YEAR [MONTHS]` and print/edit the .docx in Word.

## Data flow
```
cli.py:main (global -v/--telemetry, logging, OTEL)
  └─ cli.py:generate(month, year, months, output_dir, orientation)
      └─ calendar.py:write_calendar_doc(year, month, output_dir, orientation, months)
          ├─ month_sequence(year, month, count)          # consecutive months, cross-year
          ├─ build_document(...)                          # Document + section/page setup
          │    └─ _append_month_page(doc, y, m, orientation)
          │        ├─ month_grid(y, m)                    # Monday-first, None padding
          │        ├─ week_row_height / fitting_week_height / layout_fits   # one-page fit
          │        └─ _set_cell_border(cell)              # raw w:tcBorders OOXML
          └─ output_path(y, m, output_dir) → doc.save(str(path))  # calendar-<y>-<m>.docx
stdout: the written path; stderr: errors (typer.Exit code 1)
```

## Module ownership
| Module | Owns | Skill |
|---|---|---|
| `word_calendar_generator/calendar.py` | month grid math, page/fit math, docx rendering, file output | `calendar-layout`, `docx-rendering` |
| `word_calendar_generator/cli.py` | root Typer app, `generate` command, global flags, telemetry init | `cli-conventions` |
| `word_calendar_generator/app.py` | `make_app()` factory for command groups (help on no subcommand) | `cli-conventions` |
| `word_calendar_generator/completion.py` | `completion generate` subcommand (typer.completion) | `cli-conventions` |
| `word_calendar_generator/logging_config.py` | `-v/-vv/-vvv` levels, stderr/file handlers | `cli-conventions` |
| `word_calendar_generator/telemetry/` | OTEL config (env `OTEL_*`), exporters, service, decorators | `cli-conventions` (surface) |
| `tests/` | pure-helper tests (calendar math, completion, logging, app) | `pipeline-quality` |
| `Makefile`, `pyproject.toml`, `vulture_whitelist.py` | gates, deps, quality config | `pipeline-quality` |

## On-disk / config
- No user state, no config file; behaviour via CLI flags and `OTEL_*` env vars
  (`OTEL_ENABLED`, `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_TYPE`, `OTEL_EXPORTER_OTLP_ENDPOINT`,
  `OTEL_EXPORTER_OTLP_INSECURE` — `telemetry/config.py`).
- Output: `<output-dir>/calendar-<year>-<month>.docx`, default `~/Downloads`.
- Global install via `uv tool` (`make install-global`).

## Invariants
1. One page per month: the fit budget `2*1.5 + 2.0 + 1.0 + n*week_cm + 0.8 ≤ page height`
   (cm) must hold for 4-, 5- and 6-week months in landscape AND portrait
   (`test_week_row_height_fits_one_page`, `test_fitting_week_height_is_validated`).
2. Grid/fit math stays pure and unit-tested in `calendar.py`; rendering stays in
   `build_document`/`_append_month_page`.
3. mypy strict passes — no untyped calls (e.g. use `add_break(WD_BREAK.PAGE)`, never
   `add_page_break()`).
4. `make pipeline` green before any work is declared done; fix, never bypass.
5. stdout = data/status, stderr = errors/diagnostics; global `-v` flags precede subcommands.
6. Every command docstring ends with a runnable `\b Examples:` block (AI-agent-first).
7. New Typer entrypoints / StrEnum members / attribute assignments land in
   `vulture_whitelist.py`.

## Which skill for which change
| Change | Load |
|---|---|
| Grid math, start-of-week, fit, orientation, row heights | `calendar-layout` |
| Table styling, borders, sections, margins, page breaks, fonts | `docx-rendering` |
| Commands, options, help text, logging, completion, telemetry surface | `cli-conventions` |
| Tests, coverage, vulture, xenon, mypy, pip-audit, gitleaks, builds | `pipeline-quality` |
| Creating/refining/building FEAT stories | `story-lifecycle` |

## Known problems
- Version string is triple-sourced: `pyproject.toml:3`, `__init__.py:7` (`__version__`),
  and hardcoded in `cli.py:24` (`version_callback`) — see FEAT-2.
- No CI — gates run only locally — see FEAT-1.
- No release/versioning policy, no CHANGELOG — see FEAT-2.
