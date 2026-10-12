---
id: FEAT-3
title: Add make update target and a patching cadence
status: backlog
priority: P3
domains: [pipeline-quality]
depends_on: []
created: 2026-10-12
updated: 2026-10-12
refinement_rounds: 0
commits: []
---

# FEAT-3 — Add make update target and a patching cadence

## User story
As a maintainer, I want a one-command dependency update that runs the gates, so that
patching is routine and rollback is a revert.

## Context
No `make update` target. Known pitfall: after `uv sync` the mypyc-compiled `tomli` wheel can
crash pip-audit on Python 3.14; fix is
`uv pip install --reinstall --no-binary tomli tomli`. Rollback today = revert `uv.lock`.

## Acceptance criteria
1. Given `make update`, when run, then the lockfile is upgraded, the tomli fix is applied,
   and `make check` runs; failure exits non-zero.
2. Given an update lands, when it commits, then the CHANGELOG (FEAT-2) gets an entry and
   rollback is reverting that one commit.

## Technical design
- **pipeline-quality** — `update:` target: `uv lock --upgrade && uv sync --extra telemetry`
  + tomli reinstall + `make check`; document cadence (e.g. weekly).

## Out of scope
- Automated dependency bots (Renovate/Dependabot config may follow later).

## Test plan
- Run `make update` once; verify exit code and updated lock.

## Risks and mitigations
- Upstream breakage — cadence keeps diffs small.

## Open questions
- [ ] Which cadence (weekly / biweekly)?

## Definition of done
- [ ] Acceptance criteria met and demonstrated
- [ ] Tests added; all gates green (`make pipeline`)
- [ ] Owning domain skills, README and AGENTS.md updated
- [ ] Local commit(s) listed in `commits`

## Refinement log
- 2026-10-12 round 0: seeded from init discovery (no update target).
