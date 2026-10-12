---
name: story-lifecycle
description: >
  The lightweight ticket system of word-calendar-generator: FEAT-<n>-<slug>.md user stories
  that move backlog -> refined -> completed under .opencode/, their front matter and template,
  the Definition of Ready, the rules for what may be built, the `story` helper script, and the
  /refine, /feat-build, /feat-done, /feat-status commands. Use whenever you create, refine,
  build, finish or report on a story.
---

# story-lifecycle

## States = folders
| Folder | `status` field | Meaning | May be built? |
|---|---|---|---|
| `.opencode/backlog/` | `backlog` | idea or partly refined; open questions remain | **no** |
| `.opencode/refined/` | `refined` | user agreed it is implementable; no open questions | yes (if deps completed) |
| `.opencode/refined/` | `in-progress` | `/feat-build` started it | being built |
| `.opencode/completed/` | `done` | `/feat-done` accepted it | — |

Rules:
1. **Only refined stories are built.** `/feat-build` refuses anything outside `refined/`.
2. Any story can be refined again (`/refine FEAT-<n>`): a refined story that gains open
   questions or a big scope change moves back to `backlog/`.
3. Dependencies (`depends_on: [FEAT-1]`) must be in `completed/` before building.
4. The folder is the source of truth; `story move` keeps `status` in sync. Never edit
   `status` by hand except `in-progress` via `story set`.
5. IDs are never reused: `story next-id` scans all three folders.

## File format
`FEAT-<n>-<kebab-slug>.md`, from [template.md](template.md). Front matter keys (one per line,
`key: value`): `id, title, status, priority (P1–P3), domains ([…] of the domain skills:
architecture, calendar-layout, cli-conventions, docx-rendering, pipeline-quality),
depends_on ([FEAT-…]), created, updated, refinement_rounds, commits ([hashes])`.
Body sections: User story · Context · Acceptance criteria (Given/When/Then) · Technical
design (per domain) · Out of scope · Test plan · Risks · Open questions · Definition of done ·
Refinement log.

## Definition of Ready (replaces a fixed round count)
A story is ready when **all** hold:
1. User story names role, capability and benefit.
2. Every acceptance criterion is observable (CLI output, generated file, test result).
3. Technical design names real files/functions per domain.
4. Out of scope is explicit.
5. Test plan covers every acceptance criterion.
6. No unchecked open questions.
7. The user explicitly said it is complete.

Refinement has a floor of **2 answered rounds**, no fixed maximum. After each round the agent
scores criteria 1–6; the failing criteria *are* the next round's questions. When 1–6 pass, it
asks the user for criterion 7 instead of inventing filler questions.

## Helper script: `.opencode/bin/story`
```bash
.opencode/bin/story status                 # grouped summary (ready / in progress / blocked / backlog / completed)
.opencode/bin/story list refined
.opencode/bin/story next-id                # FEAT-<n+1>
.opencode/bin/story show FEAT-1 refined    # prints the story, exit 1 if not refined
.opencode/bin/story move FEAT-1 refined    # backlog|refined|completed; updates status + updated
.opencode/bin/story set FEAT-1 status in-progress
```
zsh, no dependencies. Commands inject its output with `` !`…` ``.

## Commands and agent
| Command | Does |
|---|---|
| `/refine <idea text | FEAT-n>` | runs the **refinement-agent** loop until the Definition of Ready holds → `refined/` or `backlog/` |
| `/feat-build FEAT-n` | injects the refined story, sets `in-progress`, builds it through the domain skills, commits |
| `/feat-done FEAT-n` | checks the definition of done, records commits, moves to `completed/` |
| `/feat-status` | bullet summary of backlog, refined and what can be worked on next |

The agent definition is `.opencode/agents/refinement-agent.md` (OpenCode primary agent).
In Claude Code the same procedure runs in the main session via `/refine`.

## Writing good stories here
- Ground every design line in the domain skills; name the domain(s) in `domains`.
- Keep stories small enough for one build session; split otherwise (new IDs, `depends_on`).
- Measure before fixing: performance stories carry numbers (startup ms, generate wall time,
  file size) in their acceptance criteria.
- Respect the invariants in `wcg-architecture` (one-page-per-month fit budget must hold in
  both orientations for 4/5/6-week months; grid/fit math stays pure and tested, rendering
  stays in `build_document`/`_append_month_page`; mypy strict; `make pipeline` green before
  done; stdout = data, stderr = errors).
