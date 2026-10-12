---
description: Accept a built FEAT story and move it from refined to completed
argument-hint: "FEAT-n"
allowed-tools: Bash(.opencode/bin/story:*), Bash(git log:*), Bash(git show:*), Read, Edit
---

# Done: $ARGUMENTS

!`.opencode/bin/story show $ARGUMENTS refined 2>&1`

1. If the output above is an error, stop: only stories in `.opencode/refined/` can be completed.
2. Walk the *Definition of done* checklist; verify each item against the repository
   (tests exist, `make pipeline` was run, skills/README updated, `commits` filled — check with
   `git log --oneline --grep "$ARGUMENTS"`). Tick the boxes that are true.
3. If anything is missing, list it and stop (the story stays in `refined/`, status `in-progress`).
4. Otherwise append a final line to the *Refinement log* (`<date> done: <one-line summary>`)
   and run `.opencode/bin/story move $ARGUMENTS completed`.
5. Show `.opencode/bin/story status` and suggest the next ready story.
