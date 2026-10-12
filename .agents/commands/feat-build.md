---
description: Build a refined FEAT story (refuses backlog stories)
argument-hint: "FEAT-n"
allowed-tools: Bash(.opencode/bin/story:*), Bash(uv run:*), Bash(make:*), Bash(uv add:*), Bash(uv sync:*), Bash(uv pip install:*), Bash(uv build:*), Bash(zsh -n:*), Bash(word-calendar-generator:*), Bash(git:*), Read, Write, Edit, Glob, Grep
---

# Build $ARGUMENTS

The story (only printed when it is in `.opencode/refined/`):

!`.opencode/bin/story show $ARGUMENTS refined 2>&1`

## Rules
1. If the output above is an error (not refined, or not found), STOP: tell the user to run
   `/refine $ARGUMENTS` first. Backlog stories are never built.
2. Check `depends_on`: every dependency must be in `.opencode/completed/`
   (`.opencode/bin/story status`); otherwise stop and report the blocker.
3. Mark it started: `.opencode/bin/story set $ARGUMENTS status in-progress`.
4. Load `wcg-architecture`, `story-lifecycle`, `pipeline-quality` and every skill in the
   story's `domains`. Make a todo list from the acceptance criteria and technical design.
5. Implement smallest-first (calendar math in `calendar.py` (grid/fit, pure) → docx rendering
   (`build_document`/`_append_month_page`/`_set_cell_border`) → CLI (`cli.py` command +
   `--help` Examples) → docs (README, skills, AGENTS.md)), respecting the invariants.
   Do not widen scope: anything new becomes a note for a new story.
6. Prove each acceptance criterion with tests or a generated-file check; run `make pipeline`
   (remember: if it fails before its install step the global binary is stale — re-run).
7. Update the owning domain skills, README and AGENTS.md where behaviour changed.
8. Commit locally (message references the id), record the hash:
   `.opencode/bin/story set $ARGUMENTS commits "[<hash>, …]"`. Do not push.
9. Report per acceptance criterion: met / how verified, and suggest `/feat-done $ARGUMENTS`.
