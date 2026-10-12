# AGENTS.md

Guidance for AI agents working in a project generated from
`cookiecutter-python-cli-uv`. Repo-specific product facts belong here as the
project grows; template-level logging/telemetry details live in `CLAUDE.md`.

## What this is
A Typer CLI (Python 3.14, uv, mypy strict, ruff) that generates printable A4
Word calendars: one page per month, a bordered 7-column Mon-Sun grid with one
tall row per week (`generate MONTH YEAR [MONTHS]`). AI-agent-first: every
command ships complete runnable examples in `--help`, and groups print help
instead of erroring on no subcommand. Start-here map: `.opencode/skills/wcg-architecture`.

## Always run before declaring work done
`make pipeline` is the single gate (format → install → lint → typecheck →
coverage → quality → security → build → install-global). Fix everything it
reports; do not bypass. `make check` is the lighter gate (no build/install).
- `make coverage` — pytest with `--cov=word_calendar_generator`, fails
  under 40% branch coverage. Prefer pure-helper tests.
- `make quality` — vulture (needs `vulture_whitelist.py`), xenon (`-b C -m C
  -a C`), radon metrics.
- gitleaks requires `brew install gitleaks` (not a Python dep).
- Run via `uv run …`, never global python/pip.

## Toolchain conventions
- **`make_app()`** (`word_calendar_generator/app.py`): use for every
  command group so `word-calendar-generator <group>` prints help.
- Type hints + docstrings on public functions. No comments.
- When adding a Typer entrypoint / StrEnum member, register it in
  `vulture_whitelist.py`.
- Completion uses `typer.completion` (Typer ≥0.27 dropped click shell APIs —
  do not import `click.shell_completion`).

## AI-agent-first CLI rules
- Every command docstring ends with a `\b Examples:` block of copy-pasteable
  commands.
- Keep request/parse logic in a pure `_helper(...)` and have the thin Typer
  command call it (that is what unit tests cover).
- Status/data → stdout; errors/diagnostics → stderr.
- Global `-v/-vv/-vvv` must precede the subcommand:
  `word-calendar-generator -v completion generate bash`, not after it.

## Knowledge domains (skills in `.opencode/skills/`)
| Skill | Covers |
|---|---|
| `wcg-architecture` | start-here map: flow, module ownership, invariants |
| `calendar-layout` | month grids, page sizing, one-page fit validator |
| `docx-rendering` | python-docx styling, borders, sections, breaks, fonts |
| `cli-conventions` | Typer wiring, help text, logging, completion, telemetry |
| `pipeline-quality` | make gates, coverage, vulture/xenon, mypy pitfalls |
| `story-lifecycle` | FEAT ticket system, Definition of Ready, /commands |

## Work items (story lifecycle)
Stories are `FEAT-<n>-<slug>.md` files under `.opencode/{backlog,refined,completed}/`;
folders are states. Commands: `/refine <idea|FEAT-n>` (refinement-agent loop until the
Definition of Ready holds), `/feat-build FEAT-n` (build + commit; updates owning skills in
the same commit), `/feat-done FEAT-n` (accept + move to completed), `/feat-status` (board
summary). **Only refined stories are built.** Board: `.opencode/bin/story status`.
When a change alters a domain's facts, update that skill in the same commit.

## Don't
- Don't construct `typer.Typer()` for groups — use `make_app()`.
- Don't reintroduce `from click.shell_completion import …`.
- Don't break the one-page fit budget (4/5/6-week months, both orientations).
- Don't build backlog stories or bypass the gates.
