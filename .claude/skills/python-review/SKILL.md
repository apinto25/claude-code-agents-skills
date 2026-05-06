---
name: python-review
description: Reviews Python code for PeP8 compliance, type hints, docstrings, and common anti-patterns. Use when the user asks to "review", "check quality", or "improve" Python code quality.
model: claude-sonnet-4-6
---

# Python code review

## Instructions

Review the specified Python code following these steps:

1. Run the validation scripts on the specified file: `python scripts/run_checks.py $ARGUMENTS` to identify style and lint issues
2. Check for missing type hints in function signatures
3. Consult `references/style-guide.md` and verify docstrings follow Google style format
4. Identify common anti-patterns:
  - Mutable default arguments
  - Unused imports
  - Functions longer than 20 lines
5. Present findings grouped by severity: errors, warnings, suggestions. For each issue show the line, the problem and the recommended fix

## Troubleshooting
Error: `ModuleNotFoundError`
Cause: Missing dependency
Solution: Run `uv add ruff mypy` before using this skill
