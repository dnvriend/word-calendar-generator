# Project init prompt — knowledge domains, story lifecycle and agent tooling

> **For:** Claude Code with Opus 5.5 (or stronger). **Produces:** a `.opencode/` system that
> lesser models (Sonnet, Haiku, local models in OpenCode) can operate safely: domain skills,
> a FEAT ticket system with a refinement agent, commands, a seeded backlog and an `AGENTS.md`.
> **Origin:** distilled from initialising `openjev-tool` and `thumbnail-lite-tool` (2026-10-09).
>
> **Usage:** open Claude Code in the target repository and run
> `Read .opencode/init/init-prompt.md and execute it for this repository.`
> (copy this file into the target repo's `.opencode/init/` first, or reference its path).

---

## 0. Your role and the rules of this run

You are the **tech lead initialising an existing codebase for agentic work**. Everything you
write will be read by weaker models that cannot re-derive what you know, so:

1. **Ground every fact in the code.** Name real files, functions, endpoints, flags, env vars
   and config keys. Before writing a fact into a skill, verify it (grep / read). A wrong fact in
   a skill is worse than a missing one — lesser models trust skills blindly.
2. **No speculation in skills.** Unknowns become open questions in a backlog story.
3. **Measure, don't guess.** Performance/memory/latency claims carry numbers and the command
   that produced them; otherwise they are suspects in a story, labelled as such.
4. **Ask the user** (interactive question tool, 2–4 decision-forcing questions with your
   recommendation first) only for what the code cannot tell you: purpose, audience,
   invariants, priorities. Batch questions; do not drip-feed.
5. **Respect the working tree.** If it is dirty, run the gates; when green, propose committing
   the pending work as a separate baseline commit before your own changes (ask first).
6. Use the todo list. Commit locally in logical commits; never push.
7. Follow the user's global instructions (CLAUDE.md): platform (ARM/Apple Silicon unless told
   otherwise), zsh-compatible scripts, uv + typed Python, Makefile with help, concise style.

---

## 1. Discovery (read before you write)

Run in parallel where possible:

```bash
git status --short; git log --oneline | head -30; git log --since=90.days --name-only --format= | sort | uniq -c | sort -rn | head -40
ls -la; cat README.md AGENTS.md CLAUDE.md 2>/dev/null | head -400
cat Makefile pyproject.toml package.json go.mod Cargo.toml 2>/dev/null | head -300
find . -path ./.git -prune -o -path ./node_modules -prune -o -path ./.venv -prune -o -type f -print | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40
ls -la .opencode .claude docs tests 2>/dev/null
```

Then read every source module's header/docstring and public API (`grep -n '^(def|class)'`
or the language equivalent), the test files (what they protect), CI config, and any design
docs. Run the existing quality gate once (`make check` or equivalent) and record the result:
the baseline tells you which gates exist and whether they are green.

Write down (for yourself) before continuing:
- what the app is, in two sentences; who uses it; how it is run (CLI, server, UI, library);
- the main data/request flow;
- module → concern ownership;
- external dependencies with state (models, databases, cloud, caches) and where they live on disk;
- invariants the code obviously relies on;
- **known problems** visible in code, logs or TODOs (each becomes a story, with evidence).

---

## 2. Knowledge domains (the skills)

### 2.1 Derive the domains
A knowledge domain is a **cluster of code that changes together for one reason** and needs
its own vocabulary. Derive them from (a) module ownership, (b) git co-change (files that
change in the same commits), (c) the data/request flow stages, (d) distinct runtimes or
surfaces (CLI, HTTP API, UI, model runtime, storage).

Rules:
- 4–9 domain skills for a typical repo. Fewer = too coarse to load cheaply; more = overlap.
- Names: `<project>-<domain>` (kebab-case, e.g. `thumbnail-compositor`, `openjev-models`).
- **Always** create `<project>-architecture` (start-here map) and `<project>-quality`
  (gates + test patterns + verification), plus `story-lifecycle` (section 3).
- Every module belongs to exactly one domain skill (the architecture skill's ownership table
  proves it).

Confirm the proposed domain list with the user in one question round (show name, covers,
modules) before writing the skills.

### 2.2 Skill file format
`.opencode/skills/<name>/SKILL.md`:

```markdown
---
name: <name>
description: >
  <What the domain covers, in nouns the user/agent will use (modules, classes, endpoints,
  concepts). End with "Use when …" naming the concrete triggers (files touched, tasks).>
---

# <name>

<Sections as needed; typical: What it is · Key types/files · Flow · How to add/change X ·
Conventions · Known problems (with story ids) · Gotchas.>
```

- The `description` is the trigger: lesser models pick skills by it. Be concrete.
- Keep `SKILL.md` under ~150 lines. Put depth in `references/<topic>.md` and add an index
  line in SKILL.md: ``- `references/api.md` — every endpoint with request/response shapes;
  read when adding or changing an endpoint.`` (progressive disclosure).
- Tables over prose; commands copy-pasteable; facts with file paths.
- "Known problems" sections link to the story that fixes them (`see FEAT-2`).

### 2.3 Mandatory skill contents
- **`<project>-architecture`** — what the app is; data/request flow diagram (ASCII);
  module ownership table (module → owns → skill); on-disk layout (config, state, caches,
  env-var overrides); numbered **invariants**; "which skill for which change".
- **`<project>-quality`** — exact gate commands (`make check`, `make pipeline`, each tool);
  what each test file protects; test patterns (fakes, tmp dirs, env isolation, no network /
  no heavy models in tests); manual verification recipes (real runtime, screenshots, soak);
  how to isolate config/state when testing against real services.
- Each other domain: the types, files and flows of that domain; how to extend it; its
  known problems.

### 2.4 Claude Code + OpenCode compatibility
Skills and commands live under `.opencode/`. Make them visible to Claude Code too:
```bash
mkdir -p .claude && ln -s ../.opencode/commands .claude/commands && ln -s ../.opencode/skills .claude/skills
```

---

## 3. The story lifecycle (ticket system)

### 3.1 Structure
```
.opencode/
├── agents/refinement-agent.md     # OpenCode primary agent (PO + tech lead)
├── backlog/   .gitkeep            # FEAT-<n>-<slug>.md, status backlog — never built
├── refined/   .gitkeep            # status refined | in-progress — buildable
├── completed/ .gitkeep            # status done
├── bin/story                      # zsh helper (chmod +x)
├── commands/{refine,feat-build,feat-done,feat-status}.md
├── skills/story-lifecycle/{SKILL.md,template.md}
├── skills/<project>-*/SKILL.md    # the domain skills
├── init/init-prompt.md            # this file
└── .gitignore
```
Create every file below **verbatim**, replacing only the placeholders:

| Placeholder | Replace with |
|---|---|
| `{{PROJECT}}` | repo name, e.g. `openjev-tool` |
| `{{PREFIX}}` | skill prefix, e.g. `openjev` |
| `{{BUILD_ORDER}}` | smallest-first layer order of this repo, e.g. `config/registry → backends → server API → CLI → UI → docs` |
| `{{EXTRA_TOOLS}}` | extra allowed tools for builds, e.g. `Bash(node --check:*), Bash(make:*)` |
| `{{TOPICS}}` | refinement topics specific to this repo (UX surfaces, data migration, perf budget …) |
| `{{INVARIANTS_SHORT}}` | one-line summary of the architecture invariants |
| `{{HARDWARE}}` | the target machine, e.g. `M4 Pro 48 GB` |

Verify afterwards: `zsh -n .opencode/bin/story && .opencode/bin/story status && .opencode/bin/story next-id`.

### 3.2 Key decisions baked into this system (keep them)
- **Folders are states**; only `refined/` may be built; IDs never reused.
- **Definition of Ready instead of a fixed round count.** A fixed minimum (we used 8) made the
  agent ask filler questions after the story was already complete (round 3). Floor = 2
  answered rounds; the failing DoR criteria *are* the next questions; when all pass, ask the
  user "complete enough to build?".
- Stories are the **episodic memory** of the project: decisions *with reasons*, a refinement
  log, build notes (deviations from the plan, with evidence), commits. Write them so a future
  session can reconstruct *why*.
- `/feat-build` updates the owning skills in the same commit — that is how durable knowledge
  reaches the skills.
- Measure-first stories: performance/memory work is split into "measure" (instrumentation +
  baseline numbers) and "fix" (with acceptance criteria in those numbers).



---

## 4. Seed the backlog

Create stories with `.opencode/bin/story next-id` + the template. **Check first** whether the
capability already exists (don't ticket what is done — mention it in AGENTS.md instead).
Base stories go to `backlog/` (they need the user's answers); a story goes to `refined/` only
when the Definition of Ready holds *and* the user agreed (e.g. the user asked you to refine it
directly from a design discussion — record that in the refinement log).

### 4.1 Base tickets (every project; adapt or skip what exists)
| Title | Core of the story |
|---|---|
| Makefile and pipeline | `make help` default; targets install, format, lint, typecheck, test, coverage, quality, security, check, pipeline, build, install-global, clean; each target defers to a script when non-trivial; one gate (`make pipeline`) agents must run before "done". |
| Quality gates | formatter + linter, strict type checking, tests with a coverage floor (start at the current value rounded down, ratchet up), dead-code check (vulture + whitelist), complexity gate (xenon/radon or equivalent), front-end syntax check for any JS. |
| Security gates | SAST (bandit or equivalent), dependency CVE scan (pip-audit / npm audit / govulncheck), secret scan (gitleaks with config), licence check of dependencies and models/assets. |
| Patching and updates | `make update` (lockfile upgrade + gates), a cadence (e.g. weekly), pinned versions for anything with state (models, DB schemas, runtimes), a CHANGELOG entry per update, rollback = revert the lock commit. |
| CI | the same `make check` in CI (GitHub Actions or the repo's CI), on the right architecture (ARM vs x86 explicitly). |
| Release and versioning | SemVer (or DateVer) decision, git tags, version single-sourced, CHANGELOG, build artefacts. |
| Observability | logging levels (-v/-vv/-vvv), log to stderr, optional file logging, telemetry if relevant; health/metrics endpoints for servers. |
| Docs, AI-first | README with install/usage tables; every CLI command with copy-pasteable `Examples:`; AGENTS.md current. |
| Configuration | one config file + env overrides, validation with clear errors, migration on schema change. |
| Error handling conventions | exit codes, stdout = data / stderr = diagnostics, HTTP error taxonomy. |
| Performance/memory baseline | measure startup, hot path latency, peak memory; record numbers; budget per invariant. |

### 4.2 Project-specific tickets
One story per **known problem** found in discovery (with the evidence: file:line, log
counts, measurements) and per obvious next feature the user mentions. Split measure/fix for
performance problems. Link related stories with `depends_on`.

---

## 5. AGENTS.md

Create or update (keep existing repo-specific content; append, don't clobber). General terms
only — details belong in the skills:

```markdown
# AGENTS.md
## What this is            — 3–5 sentences: purpose, users, surfaces, runtime.
## Always run before declaring work done — the single gate command and what it runs.
## Toolchain conventions   — language/tooling rules that apply everywhere.
## Knowledge domains (skills in `.opencode/skills/`) — table: skill | covers.
## Work items (story lifecycle) — table of /refine, /feat-build, /feat-done, /feat-status;
   "only refined stories are built"; `.opencode/bin/story status`;
   "When a change alters a domain's facts, update that skill in the same commit."
## Don't                   — the invariants phrased as prohibitions.
```

---

## 6. Things that make the system work for lesser models

- **Commands inject state** with `` !`.opencode/bin/story …` `` so the model starts from facts,
  not memory. Keep commands short, numbered, imperative, with explicit STOP conditions.
- **allowed-tools** in command front matter: the minimum the task needs.
- **Every skill description names its triggers**; every command names the skills to load.
- **Copy-pasteable commands everywhere** (skills, AGENTS.md, CLI `--help`).
- **Env isolation recipes** for anything that writes user state (config, caches) during
  tests or soak runs — a weaker model will otherwise rewrite the user's real config.
- **No time estimates** anywhere; complexity notes instead.
- Keep `.opencode/.gitignore` for OpenCode's local `node_modules`/`package.json`.
- Session-memory commands (`/dream`, `/reflect`, `/feat-prime`) are **not** part of the init;
  they are a parked design (see thumbnail-lite-tool `docs/memory-system.md`).

---

## 7. Verify and report

1. `zsh -n .opencode/bin/story`; `.opencode/bin/story status` shows the seeded board.
2. Every `SKILL.md` has `name` = folder name and a `description`; every module appears in the
   architecture ownership table; spot-check 5 facts per skill against the code.
3. `ls -la .claude` shows both symlinks.
4. The repo's gate is still green.
5. Commit: `Add domain skills, the story lifecycle and the seeded backlog` (plus a separate
   baseline commit for pre-existing work if the user agreed).
6. Report to the user (concise): domains (one line each), refined vs backlog stories, known
   problems found with evidence, open questions, and the next command
   (`/feat-build FEAT-1` or `/refine FEAT-n`).

---

## Appendix — files to create verbatim

The verbatim sources of the appendix files are the instantiated copies in this repository
(placeholders already replaced for `qwen3-tts-tool`):

- `.opencode/bin/story`
- `.opencode/skills/story-lifecycle/SKILL.md`
- `.opencode/skills/story-lifecycle/template.md`
- `.opencode/commands/refine.md`
- `.opencode/commands/feat-build.md`
- `.opencode/commands/feat-done.md`
- `.opencode/commands/feat-status.md`
- `.opencode/agents/refinement-agent.md`
- `.opencode/.gitignore`

To reuse this prompt in another repository, copy those files and re-introduce the
placeholders (`qwen3-tts-tool` → `{{PROJECT}}`, `qwen3-tts` → `{{PREFIX}}`, the build order in
`feat-build.md` → `{{BUILD_ORDER}}`, the extra tools → `{{EXTRA_TOOLS}}`, the topic list in
`refinement-agent.md` → `{{TOPICS}}`, the invariant line in `story-lifecycle/SKILL.md` →
`{{INVARIANTS_SHORT}}`).
