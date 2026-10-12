"""OpenTelemetry integration for word-calendar-generator.

This module provides observability (traces, metrics, logs) for the CLI.
Enable with --telemetry flag or OTEL_ENABLED=true environment variable.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from word_calendar_generator.telemetry.config import ExporterType, TelemetryConfig
from word_calendar_generator.telemetry.decorators import trace_span, traced
from word_calendar_generator.telemetry.service import TelemetryService

__all__ = [
    "ExporterType",
    "TelemetryConfig",
    "TelemetryService",
    "traced",
    "trace_span",
]
