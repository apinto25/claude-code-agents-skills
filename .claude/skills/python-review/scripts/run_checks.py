import subprocess
import sys

def run_checks(filepath):
    results = []

    ruff = subprocess.run(
        ["uv", "run", "ruff", "check", filepath],
        capture_output=True, text=True
    )
    if ruff.stdout:
        results.append(f"RUFF:\n{ruff.stdout}")

    mypy = subprocess.run(
        ["uv", "run", "mypy", filepath],
        capture_output=True, text=True
    )
    if mypy.stdout:
        results.append(f"MYPY:\n{mypy.stdout}")

    print("\n".join(results) if results else "No issues found.")


if __name__ == "__main__":
    run_checks(sys.argv[1])
