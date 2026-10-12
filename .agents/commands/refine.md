---
description: Refine an idea or an existing FEAT story into an implementable user story (until the Definition of Ready holds)
argument-hint: "<idea text | FEAT-n>"
agent: refinement-agent
allowed-tools: Bash(.opencode/bin/story:*), Read, Write, Edit, Glob, Grep
---

# Refine: $ARGUMENTS

Follow the refinement procedure exactly:
@.opencode/agents/refinement-agent.md

Current board:
!`.opencode/bin/story status`

Next free id: !`.opencode/bin/story next-id`

Start round 1 now for: **$ARGUMENTS**
