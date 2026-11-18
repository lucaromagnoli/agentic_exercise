from datetime import datetime
from pathlib import Path
from typing import Any

from triage.tools import PROJECT_ROOT

OUTDIR = PROJECT_ROOT / "out"
LOGFILENAME = "comms.log"


def post_update(
    text: str, max_characters: int = 600, log_file: Path = OUTDIR / LOGFILENAME
) -> dict[str, Any]:
    """Post update to the logfile."""
    if len(text) > max_characters:
        return {
            "error": f"update exceeds {max_characters} characters",
        }
    output_dir = log_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        line = f"{datetime.now().isoformat()} {text}"
        f.write(line + "\n")

    return {"status": "posted", "channel": "#incident-updates", "characters": len(text)}
