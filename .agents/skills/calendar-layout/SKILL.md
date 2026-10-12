---
name: calendar-layout
description: How month grids, page sizing and the one-page fit validator work in word-calendar-generator. Use when changing calendar math, orientation, row heights, or adding options like start-of-week.
---

# Calendar layout domain

Pure math lives in `word_calendar_generator/calendar.py`:

- `month_grid(year, month)` — Monday-first grid via `calendar.Calendar(firstweekday=0)`; `None` pads cells outside the month. A start-of-week option means parameterizing `firstweekday` and rotating `WEEKDAY_HEADERS`.
- `month_sequence(year, month, count)` — walks consecutive months across year boundaries; drives multi-month generation.
- `page_size(orientation)` — A4 edges swapped for landscape (29.7 x 21).
- One-page fit: `week_row_height` floors usable height to mm. Layout budget:
  `2*PAGE_MARGIN_CM (1.5) + TITLE_BLOCK_CM (2.0) + HEADER_ROW_CM (1.0)
   + n * week_cm + SAFETY_BLOCK_CM (0.8) <= page height`.
  `SAFETY_BLOCK_CM` reserves space for Word's mandatory trailing paragraph
  after the last table — removing it brings back an empty trailing page.
- Validator loop: `fitting_week_height` proposes a height, `layout_fits`
  validates, shrink 0.1 cm per attempt, max `MAX_RESIZE_ATTEMPTS` (5),
  then return best effort.

Rules:
- Keep grid/fit math pure (typed, tested); rendering stays in
  `_append_month_page` / `build_document`.
- Any change to the budget constants must keep
  `test_week_row_height_fits_one_page` and `test_fitting_week_height_is_validated`
  passing for 4, 5 and 6 week months in both orientations.
