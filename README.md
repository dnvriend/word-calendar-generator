# word-calendar-generator

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
A Python CLI tool

Python 3.14 · Typer · uv · AI-agent-first (`--help` has copy-pasteable examples)

## Install

```bash
git clone https://github.com/dnvriend/word-calendar-generator.git
cd word-calendar-generator
mise trust && mise install
uv sync
uv tool install .
```

```bash
word-calendar-generator --help
word-calendar-generator --version
word-calendar-generator completion generate zsh
```

## Commands

| Command | Description |
|---------|-------------|
| `completion generate <shell>` | Shell completion (bash/zsh/fish/powershell/pwsh) |

No subcommand prints help. Global `-v` / `-vv` / `-vvv` must precede the subcommand.

## Develop

```bash
uv sync
make pipeline   # format → lint → types → coverage → quality → security → install
```

Agent conventions: [AGENTS.md](AGENTS.md)

## License

MIT · Dennis Vriend
