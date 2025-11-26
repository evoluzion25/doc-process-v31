"""
docprocess_daemon.py

Lightweight watcher to automatically run doc-process-v31 on folders that
contain legal PDFs and have not yet been processed.

Design goals:
- Treat doc-process-v31 as the canonical text/OCR pipeline.
- Do NOT change any v31 logic; only orchestrate when it runs.
- Avoid re-processing the same folder repeatedly.
- Keep paths and tools exactly as current manual usage.
"""

import subprocess
import sys
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List
import json


# Use the current interpreter by default so this works both on host and in Docker
DEFAULT_PYTHON = Path(sys.executable)
DEFAULT_PIPELINE = Path(__file__).parent / "doc-process-v31.py"


@dataclass
class RunRecord:
    folder: str
    timestamp: float
    exit_code: int
    phase: str


def find_candidate_folders(root: Path) -> List[Path]:
    """
    Find folders under root that contain PDFs and are not marked as processed.

    A folder is considered a candidate if:
    - It contains at least one .pdf file (case-insensitive).
    - It does NOT contain the marker file '.docprocess_v31_done.json'.
    """
    candidates = []
    for pdf in root.rglob("*.pdf"):
        folder = pdf.parent
        if folder.name.startswith("_failed"):
            continue
        marker = folder / ".docprocess_v31_done.json"
        if not marker.exists():
            candidates.append(folder)
    # Deduplicate
    unique = sorted(set(candidates))
    return unique


def write_marker(folder: Path, record: RunRecord) -> None:
    """Write a small JSON marker recording the last run."""
    marker = folder / ".docprocess_v31_done.json"
    try:
        marker.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[WARN] Failed to write marker in {folder}: {e}")


def run_docprocess(folder: Path,
                   python_exe: Path = DEFAULT_PYTHON,
                   pipeline: Path = DEFAULT_PIPELINE,
                   phase: str = "all") -> int:
    """
    Invoke doc-process-v31 on a single folder.

    This mirrors the manual call:
    C:\\DevWorkspace\\.venv\\Scripts\\python.exe doc-process-v31.py --dir "<folder>" --phase all
    """
    cmd = [
        str(python_exe),
        str(pipeline),
        "--dir",
        str(folder),
        "--phase",
        phase,
    ]
    print(f"[INFO] Running doc-process-v31 on: {folder}")
    print(f"[INFO] Command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False)
        print(f"[INFO] doc-process-v31 exited with code {result.returncode} for {folder}")
        return result.returncode
    except Exception as e:
        print(f"[FAIL] Error running doc-process-v31 on {folder}: {e}")
        return 1


def main():
    """
    Simple polling loop:
    - root is provided as first argument, or defaults to current directory.
    - interval (seconds) as optional second argument (default 300).
    """
    if len(sys.argv) >= 2:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path.cwd()

    interval = 300
    if len(sys.argv) >= 3:
        try:
            interval = int(sys.argv[2])
        except ValueError:
            pass

    print(f"[INFO] docprocess_daemon starting")
    print(f"[INFO] Root directory: {root}")
    print(f"[INFO] Poll interval: {interval} seconds")
    print(f"[INFO] Python: {DEFAULT_PYTHON}")
    print(f"[INFO] Pipeline: {DEFAULT_PIPELINE}")

    if not root.exists():
        print(f"[FAIL] Root directory does not exist: {root}")
        sys.exit(1)

    while True:
        candidates = find_candidate_folders(root)
        if candidates:
            print(f"[INFO] Found {len(candidates)} candidate folder(s) to process")
        else:
            print("[INFO] No new folders to process")

        for folder in candidates:
            exit_code = run_docprocess(folder)
            record = RunRecord(
                folder=str(folder),
                timestamp=time.time(),
                exit_code=exit_code,
                phase="all",
            )
            write_marker(folder, record)

        print(f"[INFO] Sleeping for {interval} seconds")
        time.sleep(interval)


if __name__ == "__main__":
    main()


