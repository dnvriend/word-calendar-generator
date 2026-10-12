---
id: FEAT-5
title: Add start-of-week option to generate
status: backlog
priority: P2
domains: [calendar-layout, cli-conventions, docx-rendering]
depends_on: []
created: 2026-10-12
updated: 2026-10-12
refinement_rounds: 0
commits: []
---

# FEAT-5 — Add start-of-week option to generate

## User story
As a user, I want to choose the first day of the week (Monday or Sunday), so that the
printed calendar matches my regional/planning convention.

## Context
`calendar.py:month_grid` hardcodes `calendar.Calendar(firstweekday=0)` (Monday) and
`WEEKDAY_HEADERS` is a fixed Mon-Sun list. The `calendar-layout` skill already sketches the
design: parameterize `firstweekday` and rotate `WEEKDAY_HEADERS`.

## Acceptance criteria
1. Given `--start-of-week sunday`, when generating a month, then the first column is Sunday
   and the header row reads Sun-Sat.
2. Given no flag, when generating, then the grid is Monday-first (current behaviour unchanged).
3. Given either value, when the fit validator runs, then one-page fit still holds for 4/5/6
   -week months in both orientations.

## Technical design
- **calendar-layout** — `month_grid(year, month, firstweekday=0)`; header rotation derived
  from `firstweekday`; fit math untouched.
- **cli-conventions** — new `Orientation`-style `StartOfWeek` StrEnum option on `generate`
  with `\b Examples:`; register in `vulture_whitelist.py`.
- **docx-rendering** — `_append_month_page` accepts/propagates the header list; no styling
  changes.

## Out of scope
- Locale-dependent day names, other week starts (Saturday).

## Test plan
- Pure-helper tests: rotated headers, grid padding for Sunday-first, existing tests keep
  passing; CLI example in help.

## Risks and mitigations
- Off-by-one in padding — table-driven tests for a 4-, 5- and 6-week month per setting.

## Open questions
- [ ] Flag name: `--start-of-week monday|sunday` vs `--sunday-first`?
- [ ] Abbreviated or full day names in the header?

## Definition of done
- [ ] Acceptance criteria met and demonstrated
- [ ] Tests added; all gates green (`make pipeline`)
- [ ] Owning domain skills, README and AGENTS.md updated
- [ ] Local commit(s) listed in `commits`

## Refinement log
- 2026-10-12 round 0: seeded from user feature request during init.
