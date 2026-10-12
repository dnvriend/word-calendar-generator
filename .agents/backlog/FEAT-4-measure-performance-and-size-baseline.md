---
id: FEAT-4
title: Measure performance and size baseline
status: backlog
priority: P3
domains: [pipeline-quality, calendar-layout]
depends_on: []
created: 2026-10-12
updated: 2026-10-12
refinement_rounds: 0
commits: []
---

# FEAT-4 — Measure performance and size baseline

## User story
As a maintainer, I want recorded baseline numbers for startup and generation, so that future
changes have a budget to respect.

## Context
Measure-only story (no fix). Nothing is recorded today; claims about speed or file size are
guesses.

## Acceptance criteria
1. Given a cold and warm shell, when running `word-calendar-generator --version` 10x, then
   median startup wall time is recorded (with the command used).
2. Given `generate 10 2026 1` and `generate 10 2026 12` in both orientations, when timed,
   then median wall time and output file size are recorded in a table (docs or this story's
   build notes).

## Technical design
- **pipeline-quality** — a small zsh/uv timing script or manual hyperfine run; numbers go in
  the story and then into `wcg-architecture` known-baseline section.

## Out of scope
- Optimizations (those become separate fix stories referencing these numbers).

## Test plan
- Numbers reproducible from the recorded commands.

## Risks and mitigations
- Machine variance — record hardware (Apple Silicon M4) alongside.

## Open questions
- [ ] Where do baselines live permanently (docs/baseline.md vs skill)?

## Definition of done
- [ ] Acceptance criteria met and demonstrated
- [ ] Tests added; all gates green (`make pipeline`)
- [ ] Owning domain skills, README and AGENTS.md updated
- [ ] Local commit(s) listed in `commits`

## Refinement log
- 2026-10-12 round 0: seeded from init discovery (no measurements exist).
