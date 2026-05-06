# Google-style Docstrings Guide

## Basic format
Functions should be documented with:
- A summary line
- Args section with name, type, and description
- Returns section with type and description
- Raises section if applicable

## Correct example
def calculate_duration(minutes: int) -> str:
    """Converts minutes to a human-readable format.

    Args:
        minutes (int): Duration in minutes,
          must be a multiple of 15.

    Returns:
        str: Duration in "Xh Ym" format.

    Raises:
        ValueError: If minutes is not a multiple of 15.
    """
