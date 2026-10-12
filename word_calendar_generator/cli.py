"""CLI entry point for word-calendar-generator.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import atexit
from pathlib import Path
from typing import Annotated

import typer

from word_calendar_generator.calendar import Orientation, write_calendar_doc
from word_calendar_generator.completion import completion_app
from word_calendar_generator.logging_config import setup_logging
from word_calendar_generator.telemetry import TelemetryConfig, TelemetryService

app = typer.Typer(invoke_without_command=True)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo("word-calendar-generator version 0.1.0")
        raise typer.Exit()


def _shutdown_telemetry() -> None:
    """Shutdown telemetry on exit."""
    TelemetryService.get_instance().shutdown()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
            help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
        ),
    ] = 0,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
    telemetry: Annotated[
        bool,
        typer.Option(
            "--telemetry",
            envvar="OTEL_ENABLED",
            help="Enable OpenTelemetry observability.",
        ),
    ] = False,
) -> None:
    """A Python CLI tool

    Run a subcommand. With no subcommand, prints this help and exits.
    """
    setup_logging(verbose)

    config = TelemetryConfig.from_env()
    config.enabled = telemetry or config.enabled
    TelemetryService.get_instance().initialize(config)
    atexit.register(_shutdown_telemetry)

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


app.add_typer(completion_app, name="completion")


@app.command()
def generate(
    month: Annotated[int, typer.Argument(help="Month number 1-12, e.g. 10.")],
    year: Annotated[int, typer.Argument(help="Full year, e.g. 2026.")],
    months: Annotated[
        int,
        typer.Argument(help="Number of consecutive months, one page each (default 1)."),
    ] = 1,
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory to write the calendar to (default ~/Downloads).",
        ),
    ] = Path.home() / "Downloads",
    orientation: Annotated[
        Orientation,
        typer.Option(
            "--orientation",
            case_sensitive=False,
            help="Page orientation: landscape (default) or portrait.",
        ),
    ] = Orientation.LANDSCAPE,
) -> None:
    """Generate a printable Word calendar (Mon-Sun grid), one page per month.

    Writes <output-dir>/calendar-<year>-<month>.docx with each month name
    as title and a bordered 7-column table with one tall row per week.
    Defaults to A4 landscape; use --orientation portrait for A4 portrait.
    The optional third argument generates consecutive months (walking
    across year boundaries), e.g. 10 2026 4 -> Oct, Nov, Dec 2026, Jan 2027.

    \b Examples:
        word-calendar-generator generate 10 2026
        word-calendar-generator generate 10 2026 4
        word-calendar-generator generate 10 2026 4 --orientation portrait
        word-calendar-generator generate 10 2026 --output-dir ~/Documents
    """
    try:
        path = write_calendar_doc(year, month, output_dir, orientation, months)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(str(path))


if __name__ == "__main__":
    app()
