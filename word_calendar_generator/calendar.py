"""Pure calendar helpers and Word document generation.

The grid math is kept in pure functions (:func:`month_grid`,
:func:`output_path`) so unit tests can cover it without touching
python-docx. :func:`write_calendar_doc` renders a single-month calendar
page: a bold centered "October 2026" title followed by a bordered
7-column table (Mon..Sun) with one tall row per week.
"""

from __future__ import annotations

import calendar
import math
from datetime import date
from enum import StrEnum
from pathlib import Path

import docx
from docx.document import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Length, Pt

WEEKDAY_HEADERS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

A4_SHORT_EDGE = Cm(21.0)
A4_LONG_EDGE = Cm(29.7)

PAGE_MARGIN_CM = 1.5
TITLE_BLOCK_CM = 2.0
HEADER_ROW_CM = 1.0
SAFETY_BLOCK_CM = 0.8
MAX_RESIZE_ATTEMPTS = 5
RESIZE_STEP_CM = 0.1


class Orientation(StrEnum):
    """Page orientation for the generated calendar."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


def page_size(orientation: Orientation) -> tuple[Length, Length]:
    """Return the A4 (width, height) for the given orientation.

    Args:
        orientation: PORTRAIT or LANDSCAPE.

    Returns:
        Width and height as EMU lengths.

    Examples:
        >>> page_size(Orientation.PORTRAIT) < page_size(Orientation.LANDSCAPE)
        True
    """
    if orientation is Orientation.PORTRAIT:
        return (A4_SHORT_EDGE, A4_LONG_EDGE)
    return (A4_LONG_EDGE, A4_SHORT_EDGE)


def week_row_height(orientation: Orientation, num_weeks: int, shrink_cm: float = 0.0) -> float:
    """Return the week-row height in cm for the table, in shrink attempt `shrink_cm`.

    The table (header row plus week rows) plus the title block, a safety
    reserve for Word's trailing paragraph, and the page margins fits the
    usable page height, so the calendar occupies a single page regardless
    of orientation or week count.

    Args:
        orientation: PORTRAIT or LANDSCAPE.
        num_weeks: Number of week rows in the month grid (4-6).
        shrink_cm: Extra height to subtract per validator attempt (0.0 first).

    Returns:
        The week-row height in centimeters (floored to mm).

    Examples:
        >>> week_row_height(Orientation.PORTRAIT, 5) > 0
        True
    """
    _, page_height = page_size(orientation)
    usable_cm = (
        float(page_height.cm)
        - 2 * PAGE_MARGIN_CM
        - TITLE_BLOCK_CM
        - HEADER_ROW_CM
        - SAFETY_BLOCK_CM
        - shrink_cm
    )
    return math.floor(usable_cm * 10 / num_weeks) / 10


def layout_fits(orientation: Orientation, num_weeks: int, week_cm: float) -> bool:
    """Return True if title + table + margins + safety fit one page.

    Final validator stage used by :func:`fitting_week_height` to accept or
    reject a proposed week-row height.

    Args:
        orientation: PORTRAIT or LANDSCAPE.
        num_weeks: Number of week rows in the month grid (4-6).
        week_cm: Proposed week-row height in centimeters.

    Examples:
        >>> layout_fits(Orientation.PORTRAIT, 5, 4.7)
        True
    """
    _, page_height = page_size(orientation)
    used = 2 * PAGE_MARGIN_CM + TITLE_BLOCK_CM + HEADER_ROW_CM + num_weeks * week_cm
    return used + SAFETY_BLOCK_CM <= float(page_height.cm)


def fitting_week_height(orientation: Orientation, num_weeks: int) -> float:
    """Return a week-row height validated to fit one page.

    Tries the computed height, then shrinks by RESIZE_STEP_CM per attempt,
    at most MAX_RESIZE_ATTEMPTS times. After the final attempt the last
    computed height is returned (best effort, no break).

    Args:
        orientation: PORTRAIT or LANDSCAPE.
        num_weeks: Number of week rows in the month grid (4-6).

    Returns:
        The week-row height in centimeters that fits one page.
    """
    week_cm = 0.0
    for attempt in range(MAX_RESIZE_ATTEMPTS):
        week_cm = week_row_height(orientation, num_weeks, attempt * RESIZE_STEP_CM)
        if layout_fits(orientation, num_weeks, week_cm):
            return week_cm
    return week_cm


def month_grid(year: int, month: int) -> list[list[int | None]]:
    """Return the month as a Monday-first grid of weeks.

    Args:
        year: Full year, e.g. 2026.
        month: Month number 1-12.

    Returns:
        A list of weeks, each a list of 7 entries: the day number, or
        None when the cell falls outside this month.

    Raises:
        ValueError: If month is not in 1..12.

    Examples:
        >>> month_grid(2026, 10)[0]
        [None, None, None, 1, 2, 3, 4]
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month must be 1-12, got {month}")
    weeks = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
    return [[day if day != 0 else None for day in week] for week in weeks]


def month_sequence(year: int, month: int, count: int) -> list[tuple[int, int]]:
    """Return `count` consecutive (year, month) pairs starting at the given month.

    Args:
        year: Starting full year, e.g. 2026.
        month: Starting month number 1-12.
        count: Number of consecutive months (must be >= 1).

    Returns:
        List of (year, month) tuples, walking across year boundaries.

    Raises:
        ValueError: If month is not in 1..12 or count < 1.

    Examples:
        >>> month_sequence(2026, 10, 2)
        [(2026, 10), (2026, 11)]
        >>> month_sequence(2026, 11, 3)
        [(2026, 11), (2026, 12), (2027, 1)]
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month must be 1-12, got {month}")
    if count < 1:
        raise ValueError(f"count must be >= 1, got {count}")
    result: list[tuple[int, int]] = []
    y, m = year, month
    for _ in range(count):
        result.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return result


def output_path(year: int, month: int, output_dir: Path) -> Path:
    """Return the destination path, e.g. ~/Downloads/calendar-2026-10.docx.

    Args:
        year: Full year, e.g. 2026.
        month: Month number 1-12.
        output_dir: Directory the file is written to.

    Returns:
        The path ``<output_dir>/calendar-<year>-<month:02d>.docx``.
    """
    return output_dir / f"calendar-{year}-{month:02d}.docx"


def _set_cell_border(cell: object) -> None:
    """Apply a thin gray border on all sides of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()  # type: ignore[attr-defined]
    borders = tc_pr.makeelement(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcBorders",
        {},
    )
    for edge in ("top", "left", "bottom", "right"):
        el = borders.makeelement(
            f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{edge}",
            {"val": "single", "sz": "6", "color": "BFBFBF"},
        )
        borders.append(el)
    tc_pr.append(borders)


def build_document(year: int, month: int, orientation: Orientation, months: int = 1) -> Document:
    """Build the calendar Word document, one page per month.

    Args:
        year: Full year of the first month, e.g. 2026.
        month: Month number 1-12 of the first month.
        orientation: Page orientation (A4 portrait or landscape).
        months: Number of consecutive months (one page each).

    Returns:
        A python-docx Document with one calendar page per month.
    """
    doc = docx.Document()

    section = doc.sections[0]
    width, height = page_size(orientation)
    section.orientation = (
        WD_ORIENT.PORTRAIT if orientation is Orientation.PORTRAIT else WD_ORIENT.LANDSCAPE
    )
    section.page_width = width
    section.page_height = height
    section.top_margin = Cm(PAGE_MARGIN_CM)
    section.bottom_margin = Cm(PAGE_MARGIN_CM)
    section.left_margin = Cm(PAGE_MARGIN_CM)
    section.right_margin = Cm(PAGE_MARGIN_CM)

    for index, (y, m) in enumerate(month_sequence(year, month, months)):
        if index > 0:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        _append_month_page(doc, y, m, orientation)

    return doc


def _append_month_page(doc: Document, year: int, month: int, orientation: Orientation) -> None:
    """Append one month's title and calendar table to the document."""
    grid = month_grid(year, month)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(12)
    title.paragraph_format.line_spacing = 1.0
    run = title.add_run(f"{calendar.month_name[month]} {year}")
    run.bold = True
    run.font.size = Pt(26)
    run.font.name = "Arial"

    table = doc.add_table(rows=1 + len(grid), cols=7)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    table.rows[0].height = Cm(HEADER_ROW_CM)
    table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    week_cm = Cm(fitting_week_height(orientation, len(grid)))

    for col, header in enumerate(WEEKDAY_HEADERS):
        cell = table.rows[0].cells[col]
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        header_run = paragraph.add_run(header)
        header_run.bold = True
        header_run.font.size = Pt(16)
        header_run.font.name = "Arial"
        _set_cell_border(cell)

    for row_index, week in enumerate(grid, start=1):
        for col, day in enumerate(week):
            cell = table.rows[row_index].cells[col]
            paragraph = cell.paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if day is not None:
                day_run = paragraph.add_run(str(day))
                day_run.font.size = Pt(12)
                day_run.font.name = "Arial"
            _set_cell_border(cell)
        table.rows[row_index].height = week_cm
        table.rows[row_index].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY


def write_calendar_doc(
    year: int,
    month: int,
    output_dir: Path,
    orientation: Orientation,
    months: int = 1,
) -> Path:
    """Generate the calendar document and write it to disk.

    Args:
        year: Full year of the first month, e.g. 2026.
        month: Month number 1-12 of the first month.
        output_dir: Directory the file is written to (created if missing).
        orientation: Page orientation (A4 portrait or landscape).
        months: Number of consecutive months (one page each).

    Returns:
        The path of the written .docx file.

    Raises:
        ValueError: If month is not in 1..12 or months < 1.
    """
    path = output_path(year, month, output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    build_document(year, month, orientation, months).save(str(path))
    return path


def current_year_month(today: date | None = None) -> tuple[int, int]:
    """Return the (year, month) of today (or the given date)."""
    now = today if today is not None else date.today()
    return now.year, now.month
