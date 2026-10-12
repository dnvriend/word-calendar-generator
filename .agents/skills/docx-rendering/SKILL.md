---
name: docx-rendering
description: python-docx specifics for rendering the calendar document in word-calendar-generator. Use when editing table styling, borders, sections, margins, page breaks, or fonts.
---

# Word document rendering domain

Rendering lives in `word_calendar_generator/calendar.py`
(`build_document`, `_append_month_page`, `_set_cell_border`):

- Page setup on `doc.sections[0]`: set BOTH `orientation` and
  `page_width`/`page_height` (python-docx does not swap edges for you) plus
  1.5 cm margins.
- One page per month: `doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)`
  between months. Do NOT use `doc.add_page_break()` — it is untyped and fails
  `mypy --strict` (`no-untyped-call`).
- Row heights must use `WD_ROW_HEIGHT_RULE.EXACTLY` or Word grows rows and
  overflows the page.
- Cell borders are not exposed by python-docx; `_set_cell_border` writes
  raw `w:tcBorders` OOXML (thin, `BFBFBF` gray).
- Title paragraph: pin `space_before=0`, `space_after=12pt`,
  `line_spacing=1.0` so the 2.0 cm title reserve stays accurate.
- Typing: import `Document` from `docx.document` for annotations, use
  `docx.Document()` factory to construct; `save()` needs `str(path)`, not
  `Path`.
- Every attribute assignment vulture flags (alignment, height, margins, ...)
  must be whitelisted in `vulture_whitelist.py`.
