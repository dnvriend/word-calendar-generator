---
id: FEAT-2
title: Single-source the version and define the release policy
status: backlog
priority: P2
domains: [cli-conventions, pipeline-quality]
depends_on: []
created: 2026-10-12
updated: 2026-10-12
refinement_rounds: 0
commits: []
---

# FEAT-2 — Single-source the version and define the release policy

## User story
As a maintainer, I want one source of truth for the version and a tagging/CHANGELOG policy,
so that releases are reproducible and `--version` never lies.

## Context
The version 0.1.0 is triple-sourced: `pyproject.toml:3`, `word_calendar_generator/__init__.py:7`
(`__version__`), and a hardcoded string in `cli.py:24` (`version_callback`). No CHANGELOG,
no tags, no release policy.

## Acceptance criteria
1. Given any code change, when the version is bumped, then exactly one file is edited and
   `word-calendar-generator --version`, the built package metadata, and `__version__` agree.
2. Given a release, when it is tagged, then the tag name follows the agreed scheme and the
   CHANGELOG has an entry for it.

## Technical design
- **cli-conventions** — `cli.py:version_callback` imports `word_calendar_generator.__version__`
  instead of the literal.
- **pipeline-quality** — decide dynamic versioning (e.g. `uv-dynamic-versioning`/setuptools
  scm from tags) vs single edit in `pyproject.toml` + sync script; add `release` make target.

## Out of scope
- Publishing to PyPI.

## Test plan
- Unit test asserting `version_callback` output equals `__version__` equals pyproject version.

## Risks and mitigations
- Dynamic versioning adds toolchain complexity — a sync check in `make check` may suffice.

## Open questions
- [ ] SemVer or DateVer for this tool?
- [ ] Dynamic (git-tag-driven) or static (one-file) versioning?

## Definition of done
- [ ] Acceptance criteria met and demonstrated
- [ ] Tests added; all gates green (`make pipeline`)
- [ ] Owning domain skills, README and AGENTS.md updated
- [ ] Local commit(s) listed in `commits`

## Refinement log
- 2026-10-12 round 0: seeded from init discovery (version triple-sourced).
