"""Tests for the completion command (offline)."""

from __future__ import annotations

from typer.testing import CliRunner

from word_calendar_generator.cli import app


def test_completion_generate_bash() -> None:
    result = CliRunner().invoke(app, ["completion", "generate", "bash"])
    assert result.exit_code == 0
    assert result.stdout.strip()


def test_completion_generate_zsh() -> None:
    result = CliRunner().invoke(app, ["completion", "generate", "zsh"])
    assert result.exit_code == 0
    assert result.stdout.strip()
