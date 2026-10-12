---
description: Summarise the story board — backlog, refined, in progress, completed — and what to work on next
allowed-tools: Bash(.opencode/bin/story:*)
---

# Story status

!`.opencode/bin/story status`

Summarise the board above as a bullet list in this order:
- **Ready to build** (refined, dependencies completed) — id, title, priority; mark the top pick
  (highest priority, then lowest id) as *next*.
- **In progress** — id, title.
- **Blocked** — id, title, the missing dependency.
- **Backlog (needs refinement)** — id, title, priority; suggest which one to `/refine` next.
- **Completed** — count plus the latest three.
End with the exact next command(s), e.g. `/feat-build FEAT-3` or `/refine FEAT-4`.
