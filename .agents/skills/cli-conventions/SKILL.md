---
name: cli-conventions
description: Typer CLI wiring and AI-agent-first command conventions for word-calendar-generator. Use when adding or changing commands, options, help text, or completion.
---

# CLI conventions domain

Entrypoint: `word_calendar_generator/cli.py` (`app`), installed as
`word-calendar-generator`. Commands live on the root app; groups (like
`completion`) are built with `make_app()` from `word_calendar_generator/app.py`
so `<group>` without a subcommand prints help instead of erroring.

Rules (from AGENTS.md):
- Every command docstring ends with a `\b Examples:` block of copy-pasteable
  commands — help must be runnable without trial-and-error.
- Thin Typer commands: request/parse logic goes in a pure `_helper(...)` in the
  domain module; unit tests cover the helper, not the CLI.
- Status/data to stdout; errors to stderr (`typer.echo(..., err=True)` +
  `typer.Exit(code=1)`).
- Global `-v/-vv/-vvv` must precede the subcommand.
- New Typer entrypoints / StrEnum members go into `vulture_whitelist.py`.
- Completion uses `typer.completion`; never `click.shell_completion`.
- `generate` signature: `MONTH YEAR [MONTHS=1] [--orientation landscape|portrait]
  [--output-dir ~/Downloads]`. Defaults: landscape, 1 month, ~/Downloads.
