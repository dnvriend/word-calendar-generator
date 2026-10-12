"""Tests for calendar grid math and output-path helpers."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from word_calendar_generator.calendar import (
    HEADER_ROW_CM,
    PAGE_MARGIN_CM,
    SAFETY_BLOCK_CM,
    TITLE_BLOCK_CM,
    Orientation,
    current_year_month,
    fitting_week_height,
    layout_fits,
    month_grid,
    month_sequence,
    output_path,
    page_size,
    week_row_height,
)


def test_month_grid_october_2026_starts_on_thursday() -> None:
    assert month_grid(2026, 10)[0] == [None, None, None, 1, 2, 3, 4]


def test_month_grid_february_2026() -> None:
    grid = month_grid(2026, 2)
    assert len(grid) == 5
    assert grid[0] == [None, None, None, None, None, None, 1]
    assert grid[4] == [23, 24, 25, 26, 27, 28, None]


def test_month_grid_every_week_has_seven_cells() -> None:
    for week in month_grid(2027, 12):
        assert len(week) == 7


def test_month_grid_rejects_invalid_month() -> None:
    with pytest.raises(ValueError, match="month must be 1-12"):
        month_grid(2026, 0)


def test_output_path_format() -> None:
    assert output_path(2026, 10, Path("/tmp/dl")) == Path("/tmp/dl/calendar-2026-10.docx")


def test_output_path_zero_pads_month() -> None:
    assert output_path(2026, 1, Path("/tmp")).name == "calendar-2026-01.docx"


def test_month_sequence_single_month() -> None:
    assert month_sequence(2026, 10, 1) == [(2026, 10)]


def test_month_sequence_walks_year_boundary() -> None:
    assert month_sequence(2026, 10, 4) == [(2026, 10), (2026, 11), (2026, 12), (2027, 1)]


def test_month_sequence_wraps_december_to_january() -> None:
    assert month_sequence(2026, 12, 2) == [(2026, 12), (2027, 1)]


def test_month_sequence_rejects_invalid_input() -> None:
    with pytest.raises(ValueError, match="month must be 1-12"):
        month_sequence(2026, 13, 1)
    with pytest.raises(ValueError, match="count must be >= 1"):
        month_sequence(2026, 10, 0)


def test_current_year_month() -> None:
    assert current_year_month(date(2026, 10, 12)) == (2026, 10)


def test_page_size_portrait_is_tall() -> None:
    width, height = page_size(Orientation.PORTRAIT)
    assert width < height


def test_page_size_landscape_is_wide() -> None:
    width, height = page_size(Orientation.LANDSCAPE)
    assert width > height


def test_week_row_height_fits_one_page() -> None:
    for orientation in Orientation:
        _, page_height = page_size(orientation)
        for num_weeks in (4, 5, 6):
            used = (
                2 * PAGE_MARGIN_CM
                + TITLE_BLOCK_CM
                + HEADER_ROW_CM
                + SAFETY_BLOCK_CM
                + num_weeks * week_row_height(orientation, num_weeks)
            )
            assert used <= page_height.cm
            assert week_row_height(orientation, num_weeks) > 0


def test_fitting_week_height_is_validated() -> None:
    for orientation in Orientation:
        for num_weeks in (4, 5, 6):
            week_cm = fitting_week_height(orientation, num_weeks)
            assert layout_fits(orientation, num_weeks, week_cm)


def test_layout_fits_rejects_oversized_height() -> None:
    assert not layout_fits(Orientation.LANDSCAPE, 6, 4.5)
