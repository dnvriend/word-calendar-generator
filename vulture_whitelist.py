"""Vulture whitelist.

Vulture reports code that appears unused. Typer CLI commands (registered
dynamically via decorators / add_typer) and the make_app no-subcommand
callback show up as false positives, so they are listed here.

Reviewed manually. Do not delete entries without re-running:
    uv run vulture word_calendar_generator vulture_whitelist.py
"""

# --- Typer command entrypoints (registered dynamically, not imported) --------
main  # word_calendar_generator/cli.py — @app.callback
generate  # word_calendar_generator/cli.py — @app.command
generate_completion  # word_calendar_generator/completion.py — @completion_app.command
_show_help_when_no_subcommand  # word_calendar_generator/app.py — make_app callback

# --- Typer option params -----------------------------------------------------
version  # word_calendar_generator/cli.py — --version option param
output_dir  # word_calendar_generator/cli.py — --output-dir option param

# --- calendar.py: python-docx attribute assignments (used by Word rendering) --
alignment
bold
size
autofit
height
page_width
page_height
top_margin
bottom_margin
left_margin
right_margin
height_rule
space_before
space_after
line_spacing

# --- calendar.py: helpers kept for callers/tests ------------------------------
current_year_month

# --- TelemetryService public API (consumed by external callers) -------------
meter  # property
otel_logger  # property
reset  # method
