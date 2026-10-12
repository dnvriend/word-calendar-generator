---
id: FEAT-1
title: Add CI running make check on ARM
status: backlog
priority: P2
domains: [pipeline-quality]
depends_on: []
created: 2026-10-12
updated: 2026-10-12
refinement_rounds: 0
commits: []
---

# FEAT-1 — Add CI running make check on ARM

## User story
As a developer, I want CI to run the quality gates on every push/PR, so that regressions are
caught without relying on a local machine.

## Context
Gates exist only locally (`make check`: install, lint, typecheck, coverage, quality,
security). No `.github/workflows/` in the repo. gitleaks is a brew binary, not a Python dep —
CI needs it installed or that step adapted.

## Acceptance criteria
1. Given a push to main, when CI runs, then `make check` (or the ARM-equivalent job matrix)
   passes on a GitHub-hosted ARM runner (e.g. `ubuntu-24.04-arm`).
2. Given a PR, when CI runs, then the same gate blocks the PR on failure.
3. Given gitleaks is not pip-installable, when CI prepares the job, then it is installed
   (apt/binary download) or the step is skipped with an explicit note.

## Technical design
- **pipeline-quality** — new `.github/workflows/ci.yml`; uv setup (astral-sh/setup-uv);
  Python 3.14; `make check`.

## Out of scope
- Release pipelines, multi-OS matrices.

## Test plan
- Green run on push; a deliberately failing commit shows red (verify once on a branch).

## Risks and mitigations
- Python 3.14 availability on runners — pin via setup-uv/mise.
- tomli mypyc wheel crash under pip-audit on 3.14 — apply the documented reinstall fix in CI.

## Open questions
- [ ] Which runner (ubuntu-24.04-arm vs macos-latest) — local dev is Apple Silicon M4.
- [ ] Should `make pipeline` (incl. build + install-global) run in CI or only `make check`?

## Definition of done
- [ ] Acceptance criteria met and demonstrated
- [ ] Tests added; all gates green (`make pipeline`)
- [ ] Owning domain skills, README and AGENTS.md updated
- [ ] Local commit(s) listed in `commits`

## Refinement log
- 2026-10-12 round 0: seeded from init discovery (no CI config in repo).
