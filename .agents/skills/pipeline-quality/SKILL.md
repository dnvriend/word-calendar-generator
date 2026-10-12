---
name: pipeline-quality
description: The make pipeline quality gates for word-calendar-generator and their known pitfalls. Use when tests, coverage, vulture, xenon, mypy strict, or pip-audit fail.
---

# Pipeline & quality domain

`make pipeline` is the single gate: format → install → lint → typecheck →
coverage → quality → security → build → install-global. `make check` is the
lighter gate. Fix everything it reports; never bypass.

Pitfalls encountered in this repo:
- Coverage: `--cov=word_calendar_generator`, fails under 40% branch coverage.
  `cli.py` and `telemetry/` are omitted — cover pure helpers in tests instead.
- vulture: every python-docx attribute assignment and Typer entrypoint is a
  false positive; whitelist in `vulture_whitelist.py` (never delete entries
  without re-running `uv run vulture word_calendar_generator vulture_whitelist.py`).
- mypy strict: python-docx has partial stubs — `add_page_break()` is untyped,
  `save()` takes `str | IO[bytes]`, `Cm` is not `Emu` (both subclass `Length`).
- Long example lines in docstrings trip ruff E501 (max 100) — wrap them with `\`.
- pip-audit + Python 3.14: the mypyc-compiled `tomli` wheel crashes with
  `ModuleNotFoundError: ...__mypyc`. Fix with
  `uv pip install --reinstall --no-binary tomli tomli` (again after `uv sync`).
- If the pipeline fails before its install step, the globally installed
  `word-calendar-generator` binary is STALE — re-run the pipeline before
  verifying CLI behavior.
